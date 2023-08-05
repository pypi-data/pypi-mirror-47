#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <bp_util.h>

double rosenbrock(int nelements, double* x)
{
    double sum = 0.0;
    for(int i=0; i<nelements-2; ++i) {
        sum += 100.0*pow((x[i+1] - pow(x[i], 2)), 2) + pow((1-x[i]), 2);
    }
    return sum;
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int nelements = bp.args.sizes[0];
    const int trials = bp.args.sizes[1];

    // Create the pseudo-data
    double* dataset = (double*)malloc(sizeof(double)*nelements);

    for(int i=0; i<nelements; ++i) {
        dataset[i] = i/(double)nelements;
    }

    bp.timer_start();                               // Start timer
    double res = 0.0;
    for(int i=0; i<trials; ++i) {
        res += rosenbrock(nelements, dataset);      // Run benchmark
    }
    res /= trials;
    bp.timer_stop();                                // Stop timer
    
    bp.print("rosenbrock(c99_seq)");                // Print results..
    if (bp.args.verbose) {                          // ..and value.
        printf("Result = %f\n", res);
    }

    return 0;
}
