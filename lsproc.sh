#!/usr/bin/env bash
# Shows all running climate scripts
EXCLUDE_CURRENT_SCRIPT=$0
ps u | grep pi | egrep "\.\/.+sh" | grep -v $EXCLUDE_CURRENT_SCRIPT
