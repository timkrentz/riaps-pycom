'''
Deployment language processor
Created on Nov 7, 2016

@author: riaps
'''

from os.path import join
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx.exceptions import TextXSemanticError

import sys
import os
import argparse

class DeploymentModel(object):
    '''
    Deployment model loader/parser
    '''
    def __init__(self,fileName,debug=False):
        riaps_folder = os.getenv('RIAPSHOME', './') # RIAPSHOME points to the folder containing the grammar
        this_folder = os.getcwd()  
        # Get meta-model from language grammar
        depl_meta = metamodel_from_file(join(riaps_folder, 'riaps/lang/depl.tx'),
                                         debug=debug)       
        # Register object processors for wires and timer ports
#       depl_meta.register_obj_processors(obj_processors)
    
        # Optionally export meta-model to dot (for debugging only)
        # metamodel_export(depl_meta, join(this_folder, 'depl_meta.dot'))
        
        try:
            # Instantiate the model object structure from the model file 
            depl_model = depl_meta.model_from_file(join(this_folder, fileName))
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise
        except: 
            print ("Unexpected error:", sys.exc_info()[0])
            raise
        # Optionally export model to dot
        # model_export(depl_model, join(this_folder, 'sample.dot'))
        
        self.appName = depl_model.name
        self.deployments = []
        for dep in depl_model.actorDeployments:
            loc = dep.location
            target = []
            if loc.all:
                pass
            else:
                for host in loc.hosts:
                    target.append(host.name)
            actors = []
            for act in dep.actors:
                actObj = { }
                actObj["name"] = act.name
                actObj["actuals"] = self.getActuals(act.actuals)
                actors.append(actObj)
            self.deployments.append({"target" : target,
                                     "actors" : actors})
            
    def getActuals(self,actuals):
        res = []
        for actual in actuals:
            actualObj = { }
            actualObj["name"] = actual.argName
            # value is used in all (value) options, textX makes it a list
            actualObj["value"] = actual.argValue.value[0]
            res.append(actualObj)
        return res
    
    def getAppName(self):
        return self.appName
    
    def getDeployments(self):
        return self.deployments
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model file name")       # Model file argument
    args = parser.parse_args()
    try:
        deplo = DeploymentModel(args.model)
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    print (deplo.deployments)

