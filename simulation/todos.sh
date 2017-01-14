#!/bin/bash

find -name "*.py" -exec echo {} \; -exec grep -r "TODO" {} \;
