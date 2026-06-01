#!/bin/bash
# testing 
echo "DRH_PLUMBING_SPOOL: Flow_Rate=42GPM :: Target=Johnny5_Reclamation" | nc -u -w1 localhost 9999
