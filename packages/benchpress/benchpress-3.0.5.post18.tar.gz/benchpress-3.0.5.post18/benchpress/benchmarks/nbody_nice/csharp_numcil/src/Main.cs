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
using NumCIL;
using Utilities;

namespace nice
{
	public static class Nice
    {
		public static void Main (string[] args)
		{
			Utilities.RunBenchmark.Run(args, 3, (input) => 
				{
					var planets = input.sizes[0];
					var asteroids = input.sizes[1];
					var iterations = input.sizes[2];
					var image_output = RunBenchmark.ParseBoolOption(input.cmd_opts, "images");
					
					if (input.type == typeof(double)) 
					{
						var data = NiceSolverDouble.Create(planets, asteroids);
						if (input.use_bohrium)
							NumCIL.Bohrium.Utility.Flush();
						using (new DispTimer(string.Format("Nice (Double) {0}x{1}*{2}", planets, asteroids, iterations)))
						{
							NiceSolverDouble.Solve(data, iterations, image_output);
							//NiceSolverDouble.Sync(data);
							if (input.use_bohrium)
								NumCIL.Bohrium.Utility.Flush();
						}
					} 
					else 
					{
						var data = NiceSolverSingle.Create(planets, asteroids);
						if (input.use_bohrium)
							NumCIL.Bohrium.Utility.Flush();
						using (new DispTimer(string.Format("Nice (Single) {0}x{1}*{2}", planets, asteroids, iterations)))
						{
							NiceSolverSingle.Solve(data, iterations, image_output);
							//NiceSolverSingle.Sync(data);
							if (input.use_bohrium)
								NumCIL.Bohrium.Utility.Flush();
						}
					}
				}
			);
		}
    }
}
