__global__ void test32(){
    printf("%d, %d, %d %d %d\n",blockDim.x,blockDim.y,blockDim.z,threadIdx.x,threadIdx.y);
}
