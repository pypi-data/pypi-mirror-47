<?
#
# ifthenelse.m :: Handles piecewise constructs in expressions
#
# This file is part of Myokit
#  Copyright 2011-2018 Maastricht University, University of Oxford
#  Licensed under the GNU General Public License v3.0
#  See: http://myokit.org
#
?>% Emulate the ternary operator x = (cond) ? iftrue : iffalse
function y = ifthenelse(cond, iftrue, iffalse)
    if (cond)
        y = iftrue;
    else
        y = iffalse;
    end
end
