#####################################
# 
# 
# Check the readme.txt file for more information about this problem.
# 
# by ThMosqueiro @ March 2014
# 
######################################





# Importing libraries


# Interface to easily read fasta files
from pyfasta import Fasta

# This will make possible go through the web
from twill import commands

# Other stuff
import sys
import time




# Get the fasta name file from command line

inputfilename = sys.argv[1]
print 'Input fasta file: ', inputfilename


# Lendo arquivo de entrada

print 'Loading fasta file...'
f = Fasta(inputfilename)


# Getting all keys
KEYS = sorted( f.keys() )


# Now we will discard everything that is larger than a certain
# threshold defined by the following variable
Size_threshold = 9000

Maiores = {}
Menores = {}


# We now split them into two dictionaries depedinding on their 
# size.
for j in KEYS:
    
    if len( f[j] ) > Size_threshold:
        Maiores[ j ] = f[j]
    else:
        Menores[ j ] = f[j]

print 'Numero de maiores: ', len( Maiores )


# Writing back to hard disk our results
input2 = inputfilename.split('.fasta')[0]
arquivo = open(input2 + '_larger.fasta', 'w')


for j in sorted(Maiores.keys()):
    arquivo.write('>' + j + '\n')
    arquivo.write(str(Maiores[j]) + '\n')

arquivo.close()



# Since there's this limitation of 2000 proteins per file in 
# the server, we'll equaly distribute them into several files

Nproteinas = len( sorted(Menores.keys()) )    # Number of proteins
Narquivos = int( Nproteinas / 2000 )          # number of files





resultfilenames = []

# For each file...
for k in range(0, Narquivos):
    
    # Specific file name
    resultfilenames.append( input2 + '_' + str(k) + '_menores.fasta' )
    
    print 'Creating file ' + resultfilenames[-1]
    arquivo = open( resultfilenames[-1] , 'w')
    
    # Every protein
    for j in sorted(Menores.keys())[ 2000*k : 2000*(k+1) - 1 ]:
        arquivo.write('>' + j + '\n')
        arquivo.write(str(Menores[j]) + '\n')

    arquivo.close()







## Sending over the internet

# For each file created in the last step, we want to submit to
# the SignalP web app, wait for the results and save it in our
# hard drive.

for fastafilename in resultfilenames:
    
    inputfile = open( fastafilename , 'r' )
    inforead = inputfile.read()
    
    
    # First steps...
    print 'Accessing the web app and filling the form...'
    
    # Going to the web app page
    commands.go('http://www.cbs.dtu.dk/services/SignalP/')
    
    # Setting up a few options
    commands.fv('2','SEQPASTE',inforead)
    commands.fv('2','graphmode',[''])
    
    
    # Submiting the appropriate form
    print 'Submiting the form'
    commands.submit('13')
    
    
    # Guessing now the job id
    a = commands.show()
    b = a.split('\n')[2]
    jobid = b.split('of')[1].split('</span')[0].strip()
    
    # Constructing the url with the results...
    url2go = 'http://www.cbs.dtu.dk//cgi-bin/webface2.fcgi?jobid=' + jobid
    print 'Our results are in ' + url2go + '\n\n'
    
    # Waiting a bit for the results...
    print 'Waiting some moments for the server to complete our request!'
    time.sleep(5*60)
    
    # This timing has actually two purposes: while the results are being 
    # calculated, the script will be quiet. But also, there will be some 
    # time after the results are ready so that the server won't go overloaded.
    # Please, do not overload the server using this script!!
    
    # Going after the results...
    commands.go(url2go)
    
    
    # Following the link for the result file
    commands.follow('processed fasta entries')
    
    # Saving the result in the hard drive
    commands.save_html( fastafilename.split('.fasta')[0] + '_RESULT.fasta' )




# This is the end, my friend.
