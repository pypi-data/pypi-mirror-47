# distutils: language = c++

cimport cython
from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as np
import pycalphad.variables as v

cdef symengine.LLVMDoubleVisitor llvm_double_visitor(llvm_double_obj):
    """Use the bytes from calling reduce on an LLVMDouble object to construct an LLVMDoubleVisitor"""
    cdef symengine.LLVMDoubleVisitor f = symengine.LLVMDoubleVisitor()
    if llvm_double_obj is not None:
        f.loads(llvm_double_obj.__reduce__()[-1][-1])
    return f

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double* alloc_dof_with_parameters(double[::1] dof, double[::1] parameters) nogil:
    """Remember to free() if parameters.shape[0] > 0"""
    cdef double* dof_concat
    cdef int j
    cdef int num_dof = dof.shape[0] + parameters.shape[0]
    if parameters.shape[0] == 0:
        dof_concat = &dof[0]
    else:
        dof_concat = <double *> malloc(num_dof * sizeof(double))
        for j in range(0,dof.shape[0]):
            dof_concat[j] = dof[j]
        for j in range(dof.shape[0], num_dof):
            dof_concat[j] = parameters[j - dof.shape[0]]
    return dof_concat

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double* alloc_dof_with_parameters_vectorized(double[:, ::1] dof, double[::1] parameters) nogil:
    """Remember to free() if parameters.shape[0] > 0"""
    cdef double* dof_concat
    cdef int i, j
    cdef int num_inps = dof.shape[0]
    cdef int num_dof = dof.shape[1] + parameters.shape[0]

    if parameters.shape[0] == 0:
        dof_concat = &dof[0, 0]
    else:
        dof_concat = <double *> malloc(num_inps * num_dof * sizeof(double))
        for i in range(num_inps):
            for j in range(0,dof.shape[1]):
                dof_concat[i * num_dof + j] = dof[i, j]
            for j in range(dof.shape[1], num_dof):
                dof_concat[i * num_dof + j] = parameters[j - dof.shape[1]]
    return dof_concat


cdef public class PhaseRecord(object)[type PhaseRecordType, object PhaseRecordObject]:
    """
    This object exposes a common API to the solver so it doesn't need to know about the differences
    between Model implementations. PhaseRecords are immutable after initialization.
    """
    def __reduce__(self):
            return PhaseRecord, (self.components, self.state_variables, self.variables, np.array(self.parameters),
                                 self._ofunc, self._gfunc, self._hfunc, self._massfuncs, self._massgradfuncs,
                                 self._masshessianfuncs, self._intconsfunc, self._intjacfunc, self._intconshessfunc,
                                 self._mpconsfunc, self._mpjacfunc,
                                 self.num_internal_cons, self.num_multiphase_cons)

    def __cinit__(self, object comps, object state_variables, object variables,
                  double[::1] parameters, object ofunc, object gfunc, object hfunc,
                  object massfuncs, object massgradfuncs, object masshessianfuncs,
                  object internal_cons_func, object internal_jac_func, object internal_cons_hess_func,
                  object multiphase_cons_func, object multiphase_jac_func,
                  size_t num_internal_cons, size_t num_multiphase_cons):
        cdef:
            int var_idx, el_idx
        self.components = comps
        desired_active_pure_elements = [list(x.constituents.keys()) for x in self.components]
        desired_active_pure_elements = [el.upper() for constituents in desired_active_pure_elements for el in constituents]
        pure_elements = sorted(set(desired_active_pure_elements))
        nonvacant_elements = sorted([x for x in set(desired_active_pure_elements) if x != 'VA'])

        self.variables = variables
        self.state_variables = state_variables
        self.pure_elements = pure_elements
        self.nonvacant_elements = nonvacant_elements
        self.phase_dof = 0
        self.parameters = parameters
        self.num_internal_cons = num_internal_cons
        self.num_multiphase_cons = num_multiphase_cons

        for variable in variables:
            if not isinstance(variable, v.SiteFraction):
                continue
            self.phase_name = <unicode>variable.phase_name
            self.phase_dof += 1

        if ofunc is not None:
            self._ofunc = ofunc
            self._obj = llvm_double_visitor(ofunc)
        if gfunc is not None:
            self._gfunc = gfunc
            self._grad = llvm_double_visitor(gfunc)
        if hfunc is not None:
            self._hfunc = hfunc
            self._hess = llvm_double_visitor(hfunc)
        if internal_cons_func is not None:
            self._intconsfunc = internal_cons_func
            self._internal_cons = llvm_double_visitor(internal_cons_func)
        if internal_jac_func is not None:
            self._intjacfunc = internal_jac_func
            self._internal_jac = llvm_double_visitor(internal_jac_func)
        if internal_cons_hess_func is not None:
            self._intconshessfunc = internal_cons_hess_func
            self._internal_cons_hess = llvm_double_visitor(internal_cons_hess_func)
        if multiphase_cons_func is not None:
            self._mpconsfunc = multiphase_cons_func
            self._multiphase_cons = llvm_double_visitor(multiphase_cons_func)
        if multiphase_jac_func is not None:
            self._mpjacfunc = multiphase_jac_func
            self._multiphase_jac = llvm_double_visitor(multiphase_jac_func)
        if massfuncs is not None:
            self._massfuncs = massfuncs
            self._masses.resize(len(nonvacant_elements))
            for el_idx in range(len(nonvacant_elements)):
                self._masses[el_idx] = llvm_double_visitor(massfuncs[el_idx])
        if massgradfuncs is not None:
            self._massgradfuncs = massgradfuncs
            self._massgrads.resize(len(nonvacant_elements))
            for el_idx in range(len(nonvacant_elements)):
                self._massgrads[el_idx] = llvm_double_visitor(massgradfuncs[el_idx])
        if masshessianfuncs is not None:
            self._masshessianfuncs = masshessianfuncs
            self._masshessians.resize(len(nonvacant_elements))
            for el_idx in range(len(nonvacant_elements)):
                self._masshessians[el_idx] = llvm_double_visitor(masshessianfuncs[el_idx])

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void obj(self, double[::1] outp, double[:, ::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters_vectorized(dof, self.parameters)
        cdef int i
        cdef int num_inps = dof.shape[0]
        cdef int num_dof = dof.shape[1] + self.parameters.shape[0]

        for i in range(num_inps):
            self._obj.call(&outp[i], &dof_concat[i * num_dof])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void grad(self, double[::1] out, double[::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        self._grad.call(&out[0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void hess(self, double[:, ::1] out, double[::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        self._hess.call(&out[0,0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)


    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void internal_constraints(self, double[::1] out, double[::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        self._internal_cons.call(&out[0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void internal_jacobian(self, double[:, ::1] out, double[::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        self._internal_jac.call(&out[0, 0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void internal_cons_hessian(self, double[:, :, ::1] out, double[::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        self._internal_cons_hess.call(&out[0, 0, 0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void multiphase_constraints(self, double[::1] out, double[::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        self._multiphase_cons.call(&out[0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void multiphase_jacobian(self, double[:, ::1] out, double[::1] dof) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        self._multiphase_jac.call(&out[0, 0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void mass_obj(self, double[::1] out, double[:, ::1] dof, int comp_idx) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters_vectorized(dof, self.parameters)
        cdef int i
        cdef int num_inps = dof.shape[0]
        cdef int num_dof = dof.shape[1] + self.parameters.shape[0]
        if not self._masses.empty():
            for i in range(num_inps):
                self._masses[comp_idx].call(&out[i], &dof_concat[i * num_dof])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void mass_grad(self, double[::1] out, double[::1] dof, int comp_idx) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        if not self._massgrads.empty():
            self._massgrads[comp_idx].call(&out[0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void mass_hess(self, double[:,::1] out, double[::1] dof, int comp_idx) nogil:
        cdef double* dof_concat = alloc_dof_with_parameters(dof, self.parameters)
        if not self._masshessians.empty():
            self._masshessians[comp_idx].call(&out[0,0], &dof_concat[0])
        if self.parameters.shape[0] > 0:
            free(dof_concat)
