nosutils
========

container_trace.py:
-------------------

      This script is used to trace the docker containers that are attached to the Brocade VDX switches. The script needs to be copied to the VDX and it can be executed via python interpreter running on the switch.  
      
      Dependencies:
          "docker" module
      
      Usage:
          python container_trace.py <swarm-manager ip> <network driver name>
