﻿
#region Copyright
/*
This file is part of Bohrium and copyright (c) 2012 the Bohrium:
team <http://www.bh107.org>.

Bohrium is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 
of the License, or (at your option) any later version.

Bohrium is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the 
GNU Lesser General Public License along with Bohrium. 

If not, see <http://www.gnu.org/licenses/>.
*/
#endregion

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using R = NumCIL.Range;

namespace HeatEquation
{
	using NumCIL.Double;
	using T = System.Double;

    public static class HeatEquationSolverDouble
    {
    	public static NdArray Create(long width, long height)
    	{
			var res = Generate.Zeroes(height + 2, width + 2);

			res[R.All, R.El(0)] = -273.5f;
			res[R.All, R.El(-1)] = -273.5f;
			res[R.El(0), R.All] = 40f;
			res[R.El(-1), R.All] = -273.5f;

			return res;
    	}
    
        public static Tuple<int, NdArray> Solve(NdArray full, long? fixedIterations = null)
        {			
            var center = full[R.Slice(1, -1),  R.Slice(1, -1) ];
            var north  = full[R.Slice(1, -1),  R.Slice(0, -2) ];
            var east   = full[R.Slice(0, -2),  R.Slice(1, -1) ];
            var west   = full[R.Slice(2,  0),  R.Slice(1, -1) ];
            var south  = full[R.Slice(1, -1),  R.Slice(2,  0) ];


            if (fixedIterations != null)
            {
            	for(var i =0; i < fixedIterations.Value; i++)
            		center[R.All] = 0.2f * (center + north + east + west + south);

				return new Tuple<int, NdArray>((int)fixedIterations.Value, full);
            }
            else
            {
				T epsilon = 0.005f;
	            T delta = epsilon + 1;

	            int iteration = 0;

	            while (epsilon < delta)
	            {
					iteration++;

					var work = 0.2f * (center + north + east + west + south);
					delta = (work - center).Abs().Sum();
					center[R.All] = work;
	            }

				return new Tuple<int, NdArray>(iteration, full);
            }

        }
    }
}

namespace HeatEquation
{
	using NumCIL.Float;
	using T = System.Single;

    public static class HeatEquationSolverSingle
    {
    	public static NdArray Create(long width, long height)
    	{
			var res = Generate.Zeroes(height + 2, width + 2);

			res[R.All, R.El(0)] = -273.5f;
			res[R.All, R.El(-1)] = -273.5f;
			res[R.El(0), R.All] = 40f;
			res[R.El(-1), R.All] = -273.5f;

			return res;
    	}
    
        public static Tuple<int, NdArray> Solve(NdArray full, long? fixedIterations = null)
        {			
            var center = full[R.Slice(1, -1),  R.Slice(1, -1) ];
            var north  = full[R.Slice(1, -1),  R.Slice(0, -2) ];
            var east   = full[R.Slice(0, -2),  R.Slice(1, -1) ];
            var west   = full[R.Slice(2,  0),  R.Slice(1, -1) ];
            var south  = full[R.Slice(1, -1),  R.Slice(2,  0) ];


            if (fixedIterations != null)
            {
            	for(var i =0; i < fixedIterations.Value; i++)
            		center[R.All] = 0.2f * (center + north + east + west + south);

				return new Tuple<int, NdArray>((int)fixedIterations.Value, full);
            }
            else
            {
				T epsilon = 0.005f;
	            T delta = epsilon + 1;

	            int iteration = 0;

	            while (epsilon < delta)
	            {
					iteration++;

					var work = 0.2f * (center + north + east + west + south);
					delta = (work - center).Abs().Sum();
					center[R.All] = work;
	            }

				return new Tuple<int, NdArray>(iteration, full);
            }

        }
    }
}

