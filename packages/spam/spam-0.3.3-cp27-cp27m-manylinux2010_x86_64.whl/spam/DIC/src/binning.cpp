 #include <stdio.h>
#include <math.h>
#include <iostream>
#include "binning.hpp"
// #include <Eigen/Dense>

/* 2017-05-12 Emmanuel Roubin and Edward Ando
 * 
 *  Apply a 4x4 transformation matrix F to a subset of a 3D image.
 * 
 * Inputs:
 *   - F (4x4)
 *   - im
 *   - subim (allocated but empty)
 *   - origin of subim
 * 
 * Outputs:
 *   - ???
 * 
 * Approach:
 *   1. 
 */

/*                                  Image sizes, ZYX and images*/
void binningFloat(  int nz1,   int ny1,  int nx1, float* im,
                    int nzb,   int nyb,  int nxb, float* imBin,
                    int three,                      int* offset,
                    int binning )
{
    size_t binningu = (size_t) binning;

//     size_t nz1u = (size_t) nz1;
    size_t ny1u = (size_t) ny1;
    size_t nx1u = (size_t) nx1;
    size_t nzbu = (size_t) nzb;
    size_t nybu = (size_t) nyb;
    size_t nxbu = (size_t) nxb;

    size_t zo = offset[0];
    size_t yo = offset[1];
    size_t xo = offset[2];

    int binningCubed = binning * binning * binning;

//     printf("Offsets (ZYX): %i %i %i", zo, yo, xo);

//     #pragma omp parallel for simd
    /* iterate over binned image */
    for ( size_t zb=0; zb < nzbu; zb++ )
    {
        for ( size_t yb=0; yb < nybu; yb++ )
        {
            for ( size_t xb=0; xb < nxbu; xb++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                size_t indexB = zb * nybu * nxbu + yb * nxbu + xb;

                /* now loop over large image */
                for ( size_t zl=0; zl < binningu; zl++ )
                {
                    for ( size_t yl=0; yl < binningu; yl++ )
                    {
                        for ( size_t xl=0; xl < binningu; xl++ )
                        {
                            size_t index1 = ( binning*zb + zo) * ny1u * nx1u + ( binning*yb + yo) * nx1u + ( binning*xb + xo );
                            imBin[indexB] += im[ index1 ]/binningCubed;
                        }
                    }
                }
             }
        }
    }
}

void binningUInt(   int nz1,   int ny1,  int nx1,   unsigned short* im,
                    int nzb,   int nyb,  int nxb,   unsigned short* imBin,
                    int three,                      int* offset,
                    int binning )
{
    size_t binningu = (size_t) binning;

//     size_t nz1u = (size_t) nz1;
    size_t ny1u = (size_t) ny1;
    size_t nx1u = (size_t) nx1;
    size_t nzbu = (size_t) nzb;
    size_t nybu = (size_t) nyb;
    size_t nxbu = (size_t) nxb;

    size_t zo = offset[0];
    size_t yo = offset[1];
    size_t xo = offset[2];

//     printf("Offsets (ZYX): %i %i %i", zo, yo, xo);

//     #pragma omp parallel for simd
    /* iterate over binned image */
    for ( size_t zb=0; zb < nzbu; zb++ )
    {
        for ( size_t yb=0; yb < nybu; yb++ )
        {
            for ( size_t xb=0; xb < nxbu; xb++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                size_t indexB = zb * nybu * nxbu + yb * nxbu + xb;

                size_t sum = 0;
                int count = 0;
                /* now loop over large image */
                for ( size_t zl=0; zl < binningu; zl++ )
                {
                    for ( size_t yl=0; yl < binningu; yl++ )
                    {
                        for ( size_t xl=0; xl < binningu; xl++ )
                        {
                            size_t index1 = ( binning*zb + zo) * ny1u * nx1u + ( binning*yb + yo) * nx1u + ( binning*xb + xo );
                            sum += im[ index1 ];
                            count ++;
                        }
                    }
                }
                imBin[indexB] = sum/count;
             }
        }
    }
}


void binningChar(   int nz1,   int ny1,  int nx1, unsigned char* im,
                    int nzb,   int nyb,  int nxb, unsigned char* imBin,
                    int three,                       int* offset,
                    int binning )
{
    size_t binningu = (size_t) binning; 

//     size_t nz1u = (size_t) nz1;
    size_t ny1u = (size_t) ny1;
    size_t nx1u = (size_t) nx1;
    size_t nzbu = (size_t) nzb;
    size_t nybu = (size_t) nyb;
    size_t nxbu = (size_t) nxb;

    size_t zo = offset[0];
    size_t yo = offset[1];
    size_t xo = offset[2];

//     printf("Offsets (ZYX): %i %i %i", zo, yo, xo);

//     #pragma omp parallel for simd
    /* iterate over binned image */
    for ( size_t zb=0; zb < nzbu; zb++ )
    {
        for ( size_t yb=0; yb < nybu; yb++ )
        {
            for ( size_t xb=0; xb < nxbu; xb++ )
            {
                /* int variable to build index to 1D-images from x,y,z coordinates */
                size_t indexB = zb * nybu * nxbu + yb * nxbu + xb;

                size_t sum = 0;
                int count = 0;
                /* now loop over large image */
                for ( size_t zl=0; zl < binningu; zl++ )
                {
                    for ( size_t yl=0; yl < binningu; yl++ )
                    {
                        for ( size_t xl=0; xl < binningu; xl++ )
                        {
                            size_t index1 = ( binning*zb + zo) * ny1u * nx1u + ( binning*yb + yo) * nx1u + ( binning*xb + xo );
                            sum += im[ index1 ];
                            count ++;
                        }
                    }
                }
                imBin[indexB] = sum/count;
             }
        }
    }
}

