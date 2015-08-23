import numpy as np
import os


# Setup variables
SplitExec_str      = "Running query:"
SplitStartExec_str = "client.RMProxy"
SplitTempoJobs_str = "Tempo(ms)"
TagHeaders = [
    "File System Counters",
    "Job Counters",
    "Map-Reduce Framework",
    "Shuffle Errors",
    "File Input Format Counters",
    "File Output Format Counters"
]




def HMRlogParser(filename):
    """This function parses Hadoop MapReduce log files into a list of
    dictionaries that can then be used to conduct data analyses.

    """
    
    file = open(filename, 'r')
    
    wholeLog = file.read()
    
    # Splitting by execution
    Log_per_Exec = wholeLog.split( SplitExec_str )
    nExecs = len(Log_per_Exec) - 1

    # Creating a list of Execution Measures
    ExecMeasures = []

    
    # Parsing each execution
    for Exec in Log_per_Exec[1:]:
        
        perJobs = Exec.split( TagHeaders[0] )[1:]
    
        j = 0
        nJobs = len(perJobs)
    
        ExecMeasure = []
        
        for Job in perJobs:
            j += 1
        
            # Checking if there are time measurements
            if nJobs == j:
                Job_ = Job.split( SplitTempoJobs_str )

                # Getting the tempos()
                ExecMeasure_aux = {}
                for jobtime in Job_[1:]:
                    aux = jobtime.split(':')
                    ExecMeasure_aux[aux[0]] = float(aux[1].split('\n')[0])
                
                # The rest of the stuff...
                Job = Job_[0]

            
            Job_ = Job.split( SplitStartExec_str )[0]

            measures = {}
            aux = Job_
            
            for TagHeader in reversed(TagHeaders):
                
                measures[TagHeader] = {}
                
                aux_ = aux.split(TagHeader)
                aux = aux_[0]
                
                TagMeasures = aux_[-1].split('\n\t\t')
                
                for TagMeasure in TagMeasures[1:]:
                    aux2 = TagMeasure.split('\n')[0].split('=')
                    measures[TagHeader][aux2[0]] = float(aux2[1])

            ExecMeasure.append( measures )

        # Adding each job tempos
        ExecMeasure.append( ExecMeasure_aux )

        # Adding to the global measurements
        ExecMeasures.append( ExecMeasure )
    
    return ExecMeasures







if __name__ == "__main__":
    
    import pylab as pl
    
    TimesFiles = []
    X = []
    nfiles = 0
    
    for File in os.listdir(os.getcwd()):
        
        if File.endswith(".log"):
            X.append( float( File.split('Exemplo')[1].split('.log')[0] ) )
            
            nfiles += 1
            ExecMeasures = HMRlogParser(File)
            
            print "\n\nNumber of executions: ", len( ExecMeasures )
            j = 0
            SumPerExec = []
            for ExecMeasure in ExecMeasures:
                j += 1
                SumPerExec.append( sum( ExecMeasure[-1].values() ) )
                print "Execution %d : %d " %(j, SumPerExec[-1])

            TimesFiles.append( SumPerExec )
            print "Average: ", np.mean( SumPerExec )

    print '\n\n'
    print nfiles
    for j in range(nfiles):
        pl.plot(np.ones((3))*X[j], TimesFiles[j], 'bo',
                markersize=5., color=(0.3,0.3,1.0))
        pl.plot([X[j]], np.mean(TimesFiles[j]), 'bs',
                markersize=15., color=(0.3,0.3,1.0))

    pl.xlim(0,nfiles+1)
    pl.show()
    
