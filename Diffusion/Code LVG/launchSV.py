

import SDcombu_diff
import numpy as np
import matplotlib.pyplot as plt
import math as m
from scipy import integrate
### Parameters

# SD order
p       =  3

#Solver
# method=0 for Convection  !!!! c=/0!!!
# method=1 for Diffusion
#method=2 for Convection+Diffusion

method=    1


# Stability criterion : CFL 
CFL=       0.7

#Final time
Tfin   = 6


# Velocity c (m/s) and diffusion D (m^2/s)
c      =  1.
D      = 1.

#Initialization 
# init=0 --> Gaussian law (AVBP QPF)
#init=1 --> Rectangular step with erf function

init=0
# Gradient for initialize the erf 
grad_init=10**(-12)

#boundary conditions on the left side bcondL and the right side bcondR
#bcond*=0 for a Dirichlet BC
#bcond*=1 for a periodic BC
bcondL=0
bcondR=0
# If Dirichlet conditions specify values
yL=0
yR=0

### Computating solution
x0, sol0, x, sol, niter = SDcombu_diff.main(p,method,CFL,Tfin,c,D,init,grad_init,bcondL,bcondR,yL,yR)



# Write initialization
file=open("results_init.txt","w")
for i in range(len(x0)):
    file.write(str(x0[i])+",")
    file.write(str(sol0[i]) + "\n")

file.close()

# Write results, need to modify filename 
file = open("results_CFL="+str(CFL)+"_p="+str(p)+".txt", "w")   
yth=np.zeros(len(x))
for i in range(len(x)):
    if init==0:
        yth[i]=1/m.sqrt((4*D*Tfin/100)+1)*m.exp(-(x[i]-c*Tfin+0.1)**2/(4*D*Tfin+100))
    elif init==1:
        if method==0:
            yth[i]=(1-m.erf((x[i]-c*(Tfin+grad_init))))/2
        else:
            yth[i]=(1-m.erf((x[i]-c*(Tfin+grad_init))/(2*m.sqrt(D*(Tfin+grad_init)))))/2
    
    file.write(str(x[i])+",")
    file.write(str(yth[i])+",")
    file.write(str(sol[i]) + "\n")

file.close()


### Solution plotting
plt.plot(x0,sol0,'k-')
plt.plot(x,sol, 'r-')
plt.plot(x,yth, 'b-')
plt.legend(['Initial', 'Convected','Theoretical'])
plt.show()
