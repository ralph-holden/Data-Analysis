print('##########################################################')
print()
print('Stand-alone graphing script')
print()
print('Author: Ralph Holden')
print('Created: 23/08/2023')
print()
print('Notes:')
print('[Version 23/08/2023]')
print('Script uses loadtxt - required .dat file must be in same folder as script')
print('Analyses .dat file with single output. Written quick & simple thermodynamic data from LAMMPS')
print()
print('##########################################################')
      
print()
input('Press return to load functions')
print()

# IMPORT PACKAGES 

from pylab import *
from numpy import *
import matplotlib


# DEFINE FUNCTIONS

def extract_(filename):
    '''
    INPUTS
    
    OUTPUTS
    '''
    # settings
    skiprows = 2
    
    data = loadtxt(filename, skiprows = skiprows)
    
    use_data = []
    for i in data:
        use_data.append(i[1])
        
    print('final timestep:',data[-1][0])
    print('number of data points:',len(use_data))

    output_list = [ use_data , data[-1][0] ]
    
    return output_list


def mean_(data):
    '''
    INPUTS
    
    OUTPUTS
    '''
    total = 0
    for i in data:
        total += i
        
    mean = total / len(data)
    return mean


def max(data):
    '''
    Gives maximum of a list or array of data
    '''
    maximum = data[0]
    for n in data:
        if maximum < n:
            maximum = n
    return maximum


def min(data):
    '''
    Gives minimum of a list or array of data
    '''
    minimum = data[0]
    for n in data:
        if minimum > n:
            minimum = n
    return minimum


def gr(av = True, err = False, verticle = False, units = 'real', start_time = 0, loc = 'upper right', con = False, elwt = 'Standard'):
    '''
    Version 23/08/23
    Gives a graph from dat file
    Designed for LAMMPS simulation outputs
    Can output an average, or average w/ standard deviation
    '''
    print()
    print('# # # # # #')
    print()
    print('Graph version 23/08/2023')
    print()
    print('# # # # # #')
    print()
    
    # import data and output simple analysis (final timestep, number data points, mean) 
    filename = input('Filename (w/out .dat): ')
    
    
    extraction = extract_(filename+'.dat')
    y = extraction[0]
    fts = extraction[1]

    if start_time != 0:
        start_data = int(round(start_time*len(y)/fts))
        print('Starting data from data point', start_data)
        y = y[start_data:]
    
    if av == True:
        print('mean:',mean_(y))
    if err == True:
        print('Standard Deviation:', std(y))
    
    # Graph annotations
    figure(figsize=[12,7.5])
    ts = input('Timestep Value: ')
    ft = float(ts)*fts
    xlabel('Time (fs) [Timestep = ' + ts + ']')

    yl = input('y-axis label: ')
    if yl == 'Temperature':
        ylu = 'K'
    elif yl == 'Volume':
        ylu = 'A$^{3}$'
    elif yl == 'Pressure':
        ylu = 'atm'
    elif yl == 'Enthalpy':
        ylu = 'kJ mol$^{-1}$'
    elif yl == 'Distance':
        ylu = 'A'
    else:
        ylu = input('y-axis label units: ')
    if units != 'real':
        ylu = input('y-axis label units: ') # bug will result in non real & non T,V,P units being asked for twice
    ylabel(yl + ' (' + ylu + ')' )

    t_i = input('Title: ')
    title(t_i)
    
    pltlabel = 'Instantaneous ' + yl
    
    # output of graphs
    x = linspace(start_time,ft,len(y))
    plot(x, y, color='red',label=pltlabel)

    av_y_label = 'average ' + yl + ' = ' + str(round(mean_(y),1)) + ' ' + ylu
    
    if av == True and err == False:
        plot(linspace(start_time,ft,2),[mean_(y),mean_(y)],color='blue',label=av_y_label)

    elif err == True:
        elw = 10*len(y)/fts
        if elwt != 'Standard':
            elw = float(input('Error bar linewidth: '))
        mean_list = []
        for n in range(len(y)):
            mean_list.append(mean_(y))
        errorbar(linspace(start_time,ft,len(mean_list)),mean_list,color='blue',label=av_y_label,yerr=std(y),elinewidth=elw)
        
    if verticle == True:
        xvert = float(input('Verticle x-axis position? '))
        plot([xvert,xvert],[min(y),max(y)],color='blue',linestyle='--',linewidth=0.5)
        
    # legend location and figure save
    legend(loc = loc)
    if con == False:
        savefig(filename + '.png')
    else:
        savefig(input('Output graph filename: ') + '.png')

        
def execute():
    
    inptype = ['av', 'err', 'verticle', 'units', 'start_time', 'loc', 'con', 'elwt']
    inpval_stand  = [True, False, False, 'real', 0.0, 'upper right', False, 'Standard']
    
    v = []
    
    print('Inputs for graph settings:')
    print()
    
    for i in range(len(inptype)):
        
        ask_string = 'Argument ' + inptype[i] + ' is ' + str(inpval_stand[i])
        print(ask_string)
        ask_yn = input('Yes [y] or No [True / False / input correct]: ')
        
        
        if ask_yn == 'y':
            v = v + [inpval_stand[i]]
            
        else:
            if ask_yn == 'False':
                ask_yn = False
            elif ask_yn == 'True':
                ask_yn = True
            elif ask_yn[0] not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                ask_yn = int(ask_yn)
                print(ask_yn, type(ask_yn))
            v = v + [ask_yn]
        
        print()
        print()
    
    gr(av=v[0], err=v[1], verticle=v[2], units=v[3], start_time=v[4], loc=v[5], con=v[6], elwt=v[7])


print()
input('Functions loaded. Press return to execute graphing code.')
print()
# EXECUTE CODE

execute()

input('Task completed. Press return to view graph.')
input('Press return to close tab')