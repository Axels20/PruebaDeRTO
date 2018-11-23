#include<iostream.h>
#include<conio.h>
#include<iomanip.h>
#include<math.h>

using namespace std;

//Se debe ingresar X0=0; Y0=1; Xf=1; N=10

/**********************Se ingresa la funcion****************************/

float func(float x, float y){
  return 0.5*(1+x)*pow(y,2);
}

/**********************Reportar los Datos******************************/

void reportar(float x, float y, int i)
{cout<<setiosflags(ios::showpoint | ios::fixed);
  cout<<setiosflags(ios::right);
  cout.precision(4);
  cout<<setw(10)<<i<<setw(15)<<x<<setw(15)<<y<<endl;
}

/**********************Reportar los Datos******************************/

int menu()
{int opc;
  do
  {clrscr();
    cout<<setw(50)<<"SELECCIONE OPCION\n";
    cout<<setw(50)<<"-----------------\n"<<endl;
    cout<<"1.Metodo de Euler"<<endl;
    cout<<"2.Metodo de Runge -Kutta"<<endl;
    cout<<"3.Salir"<<endl;
    cout<<"\nSeleccione Opcion: ";cin>>opc;
  }while(opc<1 || opc>3);
  return opc;
}

/**********************Metodo de Euler******************************/

void Euler(){
  float x0,y0,xf,yf,h;
  int n,i;
  clrscr();
  cout<<setw(50)<<"Metodo de Integracion de Euler"<<endl;
  cout<<setw(50)<<"------------------------------"<<endl<<endl;
  cout<<"Ingrese el valor de x0: ";
  cin>>x0;
  cout<<"Ingrese el valor de y0: ";
  cin>>y0;
  cout<<"ingrese el valor de xf: ";
  cin>>xf;
  do{
    cout<<"Ingrese el numero de subintervalos a emplear: ";
    cin>>n;
  }while(n<=0);
  h=(xf-x0)/n;
  cout<<endl;
  cout<<setw(10)<<"I"<<setw(15)<<"Xi"<<setw(15)<<"Yi"<<endl;
  cout<<setw(10)<<"-"<<setw(15)<<"--"<<setw(15)<<"--"<<endl;
  for(i=1;i<=n;i++)
  { y0=y0+h*func(x0,y0);
    x0=x0+h;
    reportar(x0,y0,i);
  }
  cout<<"\nEl valor de Yf: "<<y0<<endl;
  getch();
}

/**********************Metodo de Runge Kutta******************************/

void Kutta(){
  float x0,y0,xf,yf,h,k1,k2,k3,k4;
  int n,i;
  clrscr();
  cout<<setw(50)<<"Metodo de Runge - Kutta"<<endl;
  cout<<setw(50)<<"-----------------------"<<endl<<endl;
  cout<<"Ingrese el valor de x0: ";
  cin>>x0;
  cout<<"Ingrese el valor de y0: ";
  cin>>y0;
  cout<<"ingrese el valor de xf: ";
  cin>>xf;
  do{
    cout<<"Ingrese el numero de subintervalos a emplear: ";
    cin>>n;
  }while(n<=0);
  h=(xf-x0)/n;
  cout<<endl;
  cout<<setw(10)<<"I"<<setw(15)<<"Xi"<<setw(15)<<"Yi"<<endl;
  cout<<setw(10)<<"-"<<setw(15)<<"--"<<setw(15)<<"--"<<endl;
  for(i=1;i<=n;i++)
  { k1=func(x0,y0);
    k2=func(x0+h/2,y0+h*k1/2);
    k3=func(x0+h/2,y0+h*k2/2);
    k4=func(x0+h,y0+h*k3);
    y0=y0+(k1+2*k2+2*k3+k4)*h/6;
    x0=x0+h;
    reportar(x0,y0,i);
  }
  cout<<"El valor de Yf: "<<y0<<endl;
  getch();
}

/**********************Terminar******************************/

void terminar()
{cout<<"\t\t\t\tSalir del Programa\n";
cout<<"\t\t\t\t------------------\n\n";
cout<<"Gracias por usar el programa"<<endl<<endl;
}

/**********************Funcion Principal******************************/

void main (void)
{int opc;
do
{clrscr();
  opc=menu();
  clrscr();
  switch(opc)
  {case 1: clrscr();Euler(); break;
    case 2: clrscr();Kutta();break;
    case 3: clrscr();terminar();break;
  }
  getch();
}
while(opc!=3);
getch();
}
