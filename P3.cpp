
#include <cstdlib>
#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main(int argc, char *argv[])
{
    //Definicion de variablesdouble 
    h,x0,x1,y0=1,y1,y[100],f[100],L,yv[100],et;
    cout<<"\n\t **Ecuaciones Diferenciales**";
    cout<<"\n\t *Metodo de Euler*";
    cout<<"\n\n Ingresa los valores que se te piden";
    cout<<"\n Ingresa h: "; 
    cin>>h;
    cout<<"\n x0: "; 
    cin>>x0;
    cout<<"\n y0: "<<y0;
    cout<<"\n\n x1: "; 
    cin>>x1;cout<<endl;
    
    //Desarrollo del Metodo de Euler
    //Calculo de limite
    L=x1/h;
    //Tabla para el Metodo
    cout<<"\n\n X \t\tY(x)Verdadero\tY(x)Euler \tEt(%)"<<endl;
    //Ciclo for para el desarrollo del metodo y que va imprimiendo los valores
    for(int i=0;i<=L;i++)
    {
            y[0]=1;
            f[i]=-(2*(pow((x0+(h*i)),3)))+(12*(pow((x0+(h*i)),2)))-(20*(x0+(h*i)))+8.5;
            y[i+1]=y[i]+(f[i]*h);
            yv[i]=-(0.5*pow((x0+(h*i)),4))+(4*pow((x0+(h*i)),3))-(10*pow((x0+(h*i)),2))+(8.5*(x0+(h*i)))+1;
            et=((yv[i]-y[i])/yv[i])*100;
            cout<<"\n"<<setiosflags(ios::fixed)<<x0+(h*i)<<"\t"<<yv[i]<<"\t"<<y[i]<<"\t"<<et;
            }
            
            cout<<endl<<endl;
            system("PAUSE");
            return EXIT_SUCCESS;
            }
