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

namespace reactiondiffusion
{

	using NumCIL.Double;
	using TArray = NumCIL.Double.NdArray;
	using TData = System.Double;

	public static class ReactionDiffusionSolverDouble
	{
		private static TArray Laplacian(TArray Z, TData dx)
		{
			var Ztop = Z[R.R(0, -2), R.R(1, -1)];
			var Zleft = Z[R.R(1, -1), R.R(0, -2)];
			var Zbottom = Z[R.R(2, 0), R.R(1, -1)];
			var Zright = Z[R.R(1, -1), R.R(2, 0)];
			var Zcenter = Z[R.R(1, -1), R.R(1, -1)];

			return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / (TData)Math.Pow(dx, 2);
		}

		public static void UpdateBondaries(TArray Z)
		{
			Z[R.El(0), R.All] = Z[R.El(1), R.All];
			Z[R.El(-1), R.All] = Z[R.El(-2), R.All];
			Z[R.All, R.El(0)] = Z[R.All, R.El(1)];
			Z[R.All, R.El(-1)] = Z[R.All, R.El(-2)];
		}

		public class Data
		{
			public TArray U;
			public TArray V;
			public long Size;
		}

		public static Data Create(long size)
		{
			return new Data()
			{
				U = Generate.Random(new long[] { size, size }),
				V = Generate.Random(new long[] { size, size }),
				Size = size
			};
		}

		public static TArray Solve(Data data, long iterations, bool image_output)
		{
			var a = (TData)2.8e-4;
			var b = (TData)5e-3;
			var tau = (TData)(0.1);
			var k = (TData)(-0.005);

			var dx = (TData)(2.0/data.Size);

			var T = (TData)10.0; // Total time
			var dt = (TData)(.9 * Math.Pow(dx,2) / 2);  // time step
			var n = (long)(T/dt);

			var U = data.U;
			var V = data.V;

			for(var step = 0L; step < iterations; step++)
			{
				if (image_output)
					Plot(data, step, iterations);

				// We compute the Laplacian of u and v.
				var deltaU = Laplacian(U, dx);
				var deltaV = Laplacian(V, dx);

				// We take the values of u and v inside the grid.
				var Uc = U[R.R(1,-1),R.R(1,-1)];
				var Vc = V[R.R(1,-1),R.R(1,-1)];

				// We update the variables.
				U[R.R(1,-1),R.R(1,-1)] = Uc + dt * (a * deltaU + Uc - Uc.Pow(3) - Vc + k);
				V[R.R(1,-1),R.R(1,-1)] = Vc + dt * (b * deltaV + Uc - Vc) / tau;
			
				// Neumann conditions: derivatives at the edges are null.
				UpdateBondaries(U);
				UpdateBondaries(V);


			}

			if (image_output)
				Plot(data, iterations, iterations);


			return U;
		}

		public static TData Sync(Data data)
		{
			return data.U.Value[0];
		}

		public static void Plot(Data data, long step, long steps)
		{
			var cm = Utilities.Render.ColorMap(System.Drawing.Color.Coral);
			var nm = Utilities.Render.Normalize<TData>(-1, 1);
			Utilities.Render.Plot<TData>(string.Format("step-{0:0000}.png", step), data.U, (x, y, v) => cm(nm(v)));
		}
	}
}

namespace reactiondiffusion
{

	using NumCIL.Float;
	using TArray = NumCIL.Float.NdArray;
	using TData = System.Single;

	public static class ReactionDiffusionSolverSingle
	{
		private static TArray Laplacian(TArray Z, TData dx)
		{
			var Ztop = Z[R.R(0, -2), R.R(1, -1)];
			var Zleft = Z[R.R(1, -1), R.R(0, -2)];
			var Zbottom = Z[R.R(2, 0), R.R(1, -1)];
			var Zright = Z[R.R(1, -1), R.R(2, 0)];
			var Zcenter = Z[R.R(1, -1), R.R(1, -1)];

			return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / (TData)Math.Pow(dx, 2);
		}

		public static void UpdateBondaries(TArray Z)
		{
			Z[R.El(0), R.All] = Z[R.El(1), R.All];
			Z[R.El(-1), R.All] = Z[R.El(-2), R.All];
			Z[R.All, R.El(0)] = Z[R.All, R.El(1)];
			Z[R.All, R.El(-1)] = Z[R.All, R.El(-2)];
		}

		public class Data
		{
			public TArray U;
			public TArray V;
			public long Size;
		}

		public static Data Create(long size)
		{
			return new Data()
			{
				U = Generate.Random(new long[] { size, size }),
				V = Generate.Random(new long[] { size, size }),
				Size = size
			};
		}

		public static TArray Solve(Data data, long iterations, bool image_output)
		{
			var a = (TData)2.8e-4;
			var b = (TData)5e-3;
			var tau = (TData)(0.1);
			var k = (TData)(-0.005);

			var dx = (TData)(2.0/data.Size);

			var T = (TData)10.0; // Total time
			var dt = (TData)(.9 * Math.Pow(dx,2) / 2);  // time step
			var n = (long)(T/dt);

			var U = data.U;
			var V = data.V;

			for(var step = 0L; step < iterations; step++)
			{
				if (image_output)
					Plot(data, step, iterations);

				// We compute the Laplacian of u and v.
				var deltaU = Laplacian(U, dx);
				var deltaV = Laplacian(V, dx);

				// We take the values of u and v inside the grid.
				var Uc = U[R.R(1,-1),R.R(1,-1)];
				var Vc = V[R.R(1,-1),R.R(1,-1)];

				// We update the variables.
				U[R.R(1,-1),R.R(1,-1)] = Uc + dt * (a * deltaU + Uc - Uc.Pow(3) - Vc + k);
				V[R.R(1,-1),R.R(1,-1)] = Vc + dt * (b * deltaV + Uc - Vc) / tau;
			
				// Neumann conditions: derivatives at the edges are null.
				UpdateBondaries(U);
				UpdateBondaries(V);


			}

			if (image_output)
				Plot(data, iterations, iterations);


			return U;
		}

		public static TData Sync(Data data)
		{
			return data.U.Value[0];
		}

		public static void Plot(Data data, long step, long steps)
		{
			var cm = Utilities.Render.ColorMap(System.Drawing.Color.Coral);
			var nm = Utilities.Render.Normalize<TData>(-1, 1);
			Utilities.Render.Plot<TData>(string.Format("step-{0:0000}.png", step), data.U, (x, y, v) => cm(nm(v)));
		}
	}
}

