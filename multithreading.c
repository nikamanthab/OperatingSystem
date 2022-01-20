#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>  //Header file for sleep(). man 3 sleep for details.
#include <pthread.h>

int a = 0, pshared;
pthread_spinlock_t lock;
// A normal C function that is executed as a thread 
// when its name is specified in pthread_create()
void *myThreadFun(void *vargp)
{
    for(int i=0; i<10; i++) {
        pthread_spin_lock(&lock);
    	a = a + 1;
    	printf("1->%d\n",a);
        pthread_spin_unlock(&lock);
    	sleep(1);
    }
    return NULL;
}
   
void *myThreadFun2(void *vargp)
{
    for(int i=0; i<10; i++) {
        pthread_spin_lock(&lock);
    	a = a + 1;
    	printf("2->%d\n",a);
        pthread_spin_unlock(&lock);
    	sleep(1);
    }
    return NULL;
}
int main()
{
    pthread_spin_init(&lock, pshared);
    pthread_t thread_id, thread_id2;
    printf("Before Thread\n");
    pthread_create(&thread_id, NULL, myThreadFun, NULL);
    pthread_create(&thread_id2, NULL, myThreadFun2, NULL);
    pthread_join(thread_id, NULL);
    pthread_join(thread_id2, NULL);
    printf("After Thread\n");
    printf("a->%d\n",a);
    exit(0);
}
