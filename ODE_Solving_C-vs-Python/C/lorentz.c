#include <stdio.h>
#include <cvodes/cvodes.h>
#include <cvodes/cvodes_dense.h>
#include <nvector/nvector_serial.h>

#define Ith(v,i)    NV_Ith_S(v,i-1)

#define NEQ   3
#define RTOL  RCONST(1.0e-6)
#define ATOL1 RCONST(7.0e-9)
#define T0    RCONST(0.0)
#define T1    RCONST(1.0)
#define TMULT RCONST(0.001)
#define NOUT  -1

static int f(realtype t, N_Vector y, N_Vector ydot);
static int check_flag(void *flagvalue, char *funcname, int opt);


/*
 *-------------------------------
 * Main Program
 *-------------------------------
 */

int main(int argc, char **argv)
{
  realtype reltol, t, tout;
  N_Vector y, abstol;
  void *cvode_mem;
  int flag;

  /* Create serial vector of length NEQ for I.C. and abstol */
  y = N_VNew_Serial(NEQ);
  abstol = N_VNew_Serial(NEQ); 

  /* Initialize y */
  Ith(y,1) = 1.0;
  Ith(y,2) = 1.0;
  Ith(y,3) = 1.0;
  
  /* Set the tolerances */
  reltol = RTOL;
  Ith(abstol,1) = ATOL1;
  Ith(abstol,2) = ATOL1;
  Ith(abstol,3) = ATOL1;

  /* Initialize and allocate solver memory */
  cvode_mem = CVodeCreate(CV_BDF, CV_NEWTON);
  if (check_flag((void *)cvode_mem, "CVodeCreate", 0)) return(1);
  
  flag = CVodeInit(cvode_mem, f, T0, y);
  if (check_flag(&flag, "CVodeInit", 1)) return(1);
  
  flag = CVodeSStolerances(cvode_mem,  1e-6, 1e-6);

  //flag = CVodeSetUserData(cvode_mem); 
  
  if (flag!=CV_SUCCESS) {
    printf("Something wrong setting the pointer to the data");
  }
  
  /* Call CVDense to specify the CVDENSE dense linear solver */
  flag = CVDense(cvode_mem, 3);
  if (check_flag(&flag, "CVDense", 1)) return(1);
  /* Set the Jacobian routine to internal estimation */
  //flag=CVDlsSetDenseJacFn(cvode_mem, NULL);
  
  if (check_flag(&flag, "CVDlsSetDenseJacFn", 1)) return(1);
  
  /* In loop, call CVode, print results, and test for error.
     Break out of loop when NOUT preset output times have been reached.  */

  tout = 1.1;
  while(1)
  {
    flag = CVode(cvode_mem, tout, y, &t, CV_NORMAL);
    
    if (check_flag(&flag, "CVode", 1)) break;
    if (flag == CV_SUCCESS)
    {
      //printf("%f %f %f %f\n", tout, Ith(y,1), Ith(y,2), Ith(y,3));
      if ( tout > 3000. ) break;
      tout += TMULT;
    }
  }

  
  /* Free y vector */
  N_VDestroy_Serial(y);
  
  /* Free integrator memory */
  CVodeFree(&cvode_mem);
  
  return(0);
}

static int f(realtype t, N_Vector y, N_Vector ydot)
{
  realtype vx, vy, vz, sigma, rho, beta;
  
  sigma = 10.;
  rho = 28.;
  beta = 8./3.;

  
  // Defining variables
  vx = Ith(y,1);
  vy = Ith(y,2);
  vz = Ith(y,3);
  
  Ith(ydot,1) = sigma*(vy - vx);
  Ith(ydot,2) = vx*( rho - vz ) - vy;
  Ith(ydot,3) = vx*vy - beta*vz;

  return(0);
}



static int check_flag(void *flagvalue, char *funcname, int opt)
{
  int *errflag;

  /* Check if SUNDIALS function returned NULL pointer - no memory allocated */
  if (opt == 0 && flagvalue == NULL) {
    fprintf(stderr, "\nSUNDIALS_ERROR: %s() failed - returned NULL pointer\n\n",
	    funcname);
    return(1); }

  /* Check if flag < 0 */
  else if (opt == 1) {
    errflag = (int *) flagvalue;
    if (*errflag < 0) {
      fprintf(stderr, "\nSUNDIALS_ERROR: %s() failed with flag = %d\n\n",
	      funcname, *errflag);
      return(1); }}

  /* Check if function returned NULL pointer - no memory allocated */
  else if (opt == 2 && flagvalue == NULL) {
    fprintf(stderr, "\nMEMORY_ERROR: %s() failed - returned NULL pointer\n\n",
	    funcname);
    return(1); }

  return(0);
}
