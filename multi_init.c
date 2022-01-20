#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>  //Header file for sleep(). man 3 sleep for details.
#include <pthread.h>

int a = 0;
// A normal C function that is executed as a thread 
// when its name is specified in pthread_create()
void *myThreadFun(void *vargp)
{
//    sleep(1);
//    while(1){
//    printf("Printing GeeksQuiz from Thread \n");
//    }
    while(1) {
    a = a+1;
    printf("1->%d\n",a);
    sleep(1);
    }
    return NULL;
}
   
void *myThreadFun2(void *vargp)
{
//    sleep(1);
//    while(1){
//    printf("Printing GeeksQuiz from Thread \n");
//    }
	while(1) {
    	a = a*2;
    printf("2->%d\n",a);
    sleep(1);
	}
    return NULL;
}
//int a = 0;
int main()
{
    pthread_t thread_id, thread_id2;
    printf("Before Thread\n");
    pthread_create(&thread_id, NULL, myThreadFun, NULL);
    //pthread_join(thread_id, NULL);
        pthread_create(&thread_id2, NULL, myThreadFun2, NULL);
	pthread_join(thread_id, NULL);
    pthread_join(thread_id2, NULL);
    printf("After Thread\n");
    exit(0);
}
