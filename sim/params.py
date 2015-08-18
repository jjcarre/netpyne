"""
sim.py 

list of model objects (paramaters and variables) to be shared across modules
Can modified manually or via arguments from main.py

Contributors: salvadordura@gmail.com
"""

from pylab import array, inf
from neuron import h # Import NEURON

loadNetParams = 0  # either load network params from file or set them here (and save to file)
loadSimParams = 0  # either load sim params from file or set them here (and save to file)

net = {}  # dictionary to store network params
sim = {}  # dictionary to store simulation params

###############################################################################
### SET NETWORK PARAMETERS
###############################################################################

if loadNetParams:  # load network params from file
    pass
else:  # set network params manually
    ## Position parameters
    net['scale'] = 1 # Size of simulation in thousands of cells
    net['cortthaldist']=3000 # Distance from relay nucleus to cortex -- ~1 cm = 10,000 um (check)
    net['corticalthick'] = 1740 # cortical thickness/depth


    ## Background input parameters
    net['useBackground'] = True # Whether or not to use background stimuli
    net['backgroundRate'] = 5 # Rate of stimuli (in Hz)
    net['backgroundRateMin'] = 0.1 # Rate of stimuli (in Hz)
    net['backgroundNumber'] = 1e10 # Number of spikes
    net['backgroundNoise'] = 1 # Fractional noise
    net['backgroundWeight'] = 0.1*array([1,0.1]) # Weight for background input for E cells and I cells
    net['backgroundReceptor'] = 'NMDA' # Which receptor to stimulate


    # simType is used to select between the population and conn params for different types of models (simple HH vs M1 izhikevich)
    simType = 'mpiHHTut' # 'mpiHHTut' or 'M1model'
    #simType = 'M1model' # 'mpiHHTut' or 'M1model'


    # mpiHHTut
    if simType == 'mpiHHTut':
        net['ncell']   = 100  
        net['popParams'] = []  # create list of populations - each item will contain dict with pop params

        net['popParams'].append({'cellModel': 'HH', 'numCells': net['ncell']}) # add dict with params for this pop
        
        ## Connectivity parameters
        net['connType'] = 'random'
        net['numReceptors'] = 1
        net['maxcons']   = 20                   # number of connections onto each cell
        net['weight']    = 0.004                # weight of each connection
        net['delaymean'] = 13.0                 # mean of delays
        net['delayvar']  = 1.4                  # variance of delays
        net['delaymin']  = 0.2                  # miniumum delays
        net['threshold'] = 10.0                 # threshold 


    # yfrac-based M1 model
    elif simType == 'M1model':
        net['popParams'] = []  # create list of populations, where each item contains a dict with the pop params

                       # popid, cell model,     EorI, topClass, subClass, yfracRange,     density,                
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'E', 'topClass':'IT', 'subClass':'other', 'yfracRange':[0.1, 0.26], 'density':lambda y:2e3*y}) #  L2/3 IT
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'E', 'topClass':'IT', 'subClass':'other', 'yfracRange':[0.26, 0.31], 'density':lambda y:2e3*y}) #  L4 IT
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'E', 'topClass':'IT', 'subClass':'other', 'yfracRange':[0.31, 0.52], 'density':lambda y:2e3*y}) #  L5A IT
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'E', 'topClass':'IT', 'subClass':'other', 'yfracRange':[0.52, 0.77], 'density':lambda y:2e3*y}) #  L5B IT
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'E', 'topClass':'PT', 'subClass':'other', 'yfracRange':[0.52, 0.77], 'density':lambda y:2e3*y}) #  L5B PT
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'E', 'topClass':'IT', 'subClass':'other', 'yfracRange':[0.77, 1.0], 'density':lambda y:1e3}) #  L6 IT
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'I', 'topClass':'Pva', 'subClass':'Basket', 'yfracRange':[0.1, 0.31], 'density':lambda y:1e3}) #  L2/3 Pva (LTS)
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'I', 'topClass':'Sst', 'subClass':'Marti', 'yfracRange':[0.1, 0.31], 'density':lambda y:2e3*y}) #  L2/3 Sst (FS)
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'I', 'topClass':'Pva', 'subClass':'Basket', 'yfracRange':[0.31, 0.77], 'density':lambda y:0.5e3}) #  L5 Pva (FS)
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'I', 'topClass':'Sst', 'subClass':'Marti', 'yfracRange':[0.31, 0.77], 'density':lambda y:0.5e3}) #  L5 Sst (LTS)
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'I', 'topClass':'Pva', 'subClass':'Basket', 'yfracRange':[0.77, 1.0], 'density':lambda y:0.5e3}) #  L6 Pva (FS)
        net['popParams'].append({'cellModel':'Izhi2007b', 'EorI':'I', 'topClass':'Sst', 'subClass':'Marti', 'yfracRange':[0.77, 1.0], 'density':lambda y:0.5e3}) #  L6 Sst (LTS)

        
        ## Connectivity parameters
        net['connType'] = 'yfrac'
        net['numReceptors'] = 1 
        net['useconnprobdata'] = True # Whether or not to use connectivity data
        net['useconnweightdata'] = True # Whether or not to use weight data
        net['mindelay'] = 2 # Minimum connection delay, in ms
        net['velocity'] = 100 # Conduction velocity in um/ms (e.g. 50 = 0.05 m/s)
        net['modelsize'] = 1000*net['scale'] # Size of network in um (~= 1000 neurons/column where column = 500um width)
        net['sparseness'] = 0.1 # fraction of cells represented (num neurons = density * modelsize * sparseness)
        net['scaleconnweight'] = 0.00025*array([[2, 1], [2, 0.1]]) # Connection weights for EE, EI, IE, II synapses, respectively
        net['receptorweight'] = [1, 1, 1, 1, 1] # Scale factors for each receptor
        net['scaleconnprob'] = 1/net['scale']*array([[1, 1], [1, 1]]) # scale*1* Connection probabilities for EE, EI, IE, II synapses, respectively -- scale for scale since size fixed
        net['connfalloff'] = 100*array([2, 3]) # Connection length constants in um for E and I synapses, respectively
        net['toroidal'] = False # Whether or not to have toroidal topology


        # class variables to store matrix of connection probabilities (constant or function) for pre and post cell topClass
        # net['connProbs'] = []  # create list of connectivity rules
        # net['connProbs'].append({('topClass','IT','topClass','IT'): (lambda x,y: 0.1*x+0.01/y)})  # option 1: list of dict with single tuple key and value
        # net['connProbs'].append({('topClass','IT','topClass','PT'): (lambda x,y: 0.02*x+0.01*y)}) 

        # net['connProbs'] = {}  # dict of conn rules
        # net['connProbs'][('topClass','IT','topClass','PT')] = (lambda x,y: 0.1*x+0.01/y)  # option 2: single dict with multiple tuple keys and values
        # net['connProbs'][('topClass','IT','topClass','PT')] = (lambda x,y: 0.02*x+0.01*y) 


        # net['connProbs'] = []  # create list of connectivity rules
        # net['connProbs'].append({'preTag':'topClass', 'preValue':'IT', 'postTag': 'topClass', 'postValue':'IT', 'connFunc': (lambda x,y: 0.1*x+0.01/y)})
        # net['connProbs'].append({'preTags':['topClass','subClass'], 'preValues':['IT','other'], 'postTags': ['topClass'], 'postValues':['IT'], 'connFunc': lambda x,y: 0.1*x+0.01/y})


        net['connRules'] = []  # create list of connectivity rules
        net['connRules'].append({'preTags':['topClass'], 'preValues':['IT'], 'postTags':['topClass'], 'postValues':['IT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prey,posty: 1), 'receptor':'AMPA'})  # IT->IT rule

        net['connRules'].append({'preTags':['topClass'], 'preValues':['IT'], 'postTags':['topClass'], 'postValues':['PT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prey,posty: 1), 'receptor':'AMPA'})  # IT->PT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['IT'], 'postTags':['topClass'], 'postValues':['CT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prey,posty: 1), 'receptor':'AMPA'})  # IT->CT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['IT'], 'postTags':['topClass'], 'postValues':['Pva'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prey,posty: 1), 'receptor':'AMPA'})  # IT->Pva rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['IT'], 'postTags':['topClass'], 'postValues':['Sst'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prey,posty: 1), 'receptor':'AMPA'})  # IT->Sst rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['PT'], 'postTags':['topClass'], 'postValues':['IT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prey,posty: 1), 'receptor':'AMPA'})  # PT->IT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['PT'], 'postTags':['topClass'], 'postValues':['PT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prey,posty: 1), 'receptor':'AMPA'})  # PT->PT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['PT'], 'postTags':['topClass'], 'postValues':['CT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda prex,posty: 1), 'receptor':'AMPA'})  # PT->CT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['PT'], 'postTags':['topClass'], 'postValues':['Pva'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # PT->Pva rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['PT'], 'postTags':['topClass'], 'postValues':['Sst'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # PT->Sst rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['CT'], 'postTags':['topClass'], 'postValues':['IT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # CT->IT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['CT'], 'postTags':['topClass'], 'postValues':['PT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # CT->PT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['CT'], 'postTags':['topClass'], 'postValues':['CT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # CT->CT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['CT'], 'postTags':['topClass'], 'postValues':['Pva'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # CT->Pva rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['CT'], 'postTags':['topClass'], 'postValues':['Sst'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # CT->Sst rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Pva'], 'postTags':['topClass'], 'postValues':['IT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Pva->IT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Pva'], 'postTags':['topClass'], 'postValues':['PT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Pva->PT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Pva'], 'postTags':['topClass'], 'postValues':['CT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Pva->CT rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Pva'], 'postTags':['topClass'], 'postValues':['Pva'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Pva->Pva rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Pva'], 'postTags':['topClass'], 'postValues':['Sst'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Pva->Sst rule
        
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Sst'], 'postTags':['topClass'], 'postValues':['IT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Sst->IT rule
  
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Sst'], 'postTags':['topClass'], 'postValues':['PT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Sst->PT rule             
 
        net['connRules'].append({'preTags':['topClass'], 'preValues':['Sst'], 'postTags':['topClass'], 'postValues':['CT'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Sst->CT rule

        net['connRules'].append({'preTags':['topClass'], 'preValues':['Sst'], 'postTags':['topClass'], 'postValues':['Pva'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Sst->Pva rule

        net['connRules'].append({'preTags':['topClass'], 'preValues':['Sst'], 'postTags':['topClass'], 'postValues':['Sst'], \
            'connProb':(lambda prey,posty: 0.1*prey+0.01/posty), \
            'connWeight':(lambda x,y: 1), 'receptor':'AMPA'})  # Sst->Sst rule



###############################################################################
### SET SIMULATION PARAMETERS
###############################################################################

if loadSimParams:  # load network params from file
    pass
else:
    ## Recording 
    if simType == 'mpiHHTut':
        sim['recdict'] = {'Vsoma':'soma(0.5)._ref_v'}
    elif simType == 'M1model':
        sim['recdict'] = {'V':'sec(0.5)._ref_v', 'u':'m._ref_u', 'I':'m._ref_i'}


    # Simulation parameters
    sim['duration'] = sim['tstop'] = 1*1e3 # Duration of the simulation, in ms
    h.dt = sim['dt'] = 0.5 # Internal integration timestep to use
    sim['recordStep'] = 10 # Step size in ms to save data (eg. V traces, LFP, etc)
    sim['saveFileStep'] = 1000 # step size in ms to save data to disk
    sim['randseed'] = 1 # Random seed to use


    ## Saving and plotting parameters
    sim['filename'] = '../data/m1ms'  # Set file output name
    sim['savemat'] = True # Whether or not to write spikes etc. to a .mat file
    sim['savetxt'] = False # save spikes and conn to txt file
    sim['savedpk'] = True # save to a .dpk pickled file
    sim['recordTraces'] = True  # whether to record cell traces or not
    #lfppops = [[ER2], [ER5], [EB5], [ER6]] # Populations for calculating the LFP from
    sim['saveBackground'] = False # save background (NetStims) inputs
    sim['verbose'] = 0 # Whether to write nothing (0), diagnostic information on events (1), or everything (2) a file directly from izhi.mod
    sim['plotraster'] = True # Whether or not to plot a raster
    sim['plotpsd'] = False # plot power spectral density
    sim['maxspikestoplot'] = 3e8 # Maximum number of spikes to plot
    sim['plotconn'] = False # whether to plot conn matrix
    sim['plotweightchanges'] = False # whether to plot weight changes (shown in conn matrix)
    sim['plot3darch'] = False # plot 3d architecture


    ## Stimulus parameters
    sim['usestims'] = False # Whether or not to use stimuli at all
    sim['ltptimes']  = [5, 10] # Pre-microstim touch times
    sim['ziptimes'] = [10, 15] # Pre-microstim touch times
