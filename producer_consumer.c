#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <semaphore.h>

pthread_mutex_t mutex;
int pshared_p, pshared_c, N = 10, count;
sem_t sem_c, sem_p;
pthread_t thread_id_p1, thread_id_p2, thread_id_c1, thread_id_c2;
char buffer[10][100];
int head_ptr = 0, tail_ptr = 0;
FILE *in_file;
FILE *out_file;
char * line = NULL;
size_t len = 0;
ssize_t read_line;

int write_to_buffer(head_ptr){
    if ((read_line = getline(&line, &len, in_file)) != -1) {
        printf("Retrieved line of length %zu:\n", read_line);
        printf("%s", line);
    }
    
    strcpy(buffer[head_ptr], line);
    return read_line;
}

void *read_from_buffer(tail_ptr){
    char* string = buffer[tail_ptr];
        out_file = fopen("./output.txt", "a");
    fprintf(out_file, "%s", string);
    fflush(out_file);
        fclose(out_file);

    return NULL;
}

void *producer(void *vargp){
    int repeat = 1;
    while(repeat > 0){
        printf("p");
        sem_wait(&sem_p);
        while(pthread_mutex_lock(&mutex)!=0);
        count = count+1;
        repeat = write_to_buffer(head_ptr);
        head_ptr = (head_ptr+1)%N;
        pthread_mutex_unlock(&mutex);
        sem_post(&sem_p);
        sleep(1);
    }
    return NULL;
}
void *consumer(void *vargp){
    while(1){
        printf("%d->%d\n",head_ptr,tail_ptr);
        if(head_ptr == (tail_ptr+1)%N ) {sleep(1);continue;}
        sem_wait(&sem_c);
        while(pthread_mutex_lock(&mutex)!=0);
        read_from_buffer(tail_ptr);
        tail_ptr = (tail_ptr+1)%N;
        pthread_mutex_unlock(&mutex);
        sem_post(&sem_c);
        sleep(1);
    }
    return NULL;
}

void main(){
    in_file = fopen("./input.txt", "r");
    out_file = fopen("./output.txt", "w");
    fclose(out_file);
    sem_init(&sem_p, pshared_p, N);
    sem_init(&sem_c, pshared_c, N);
    count = 0;
    pthread_create(&thread_id_p1, NULL, producer, NULL);
    // pthread_create(&thread_id_p2, NULL, producer, NULL);
    pthread_create(&thread_id_c1, NULL, consumer, NULL);
    // pthread_create(&thread_id_c2, NULL, consumer, NULL);

    pthread_join(thread_id_p1, NULL);
    // pthread_join(thread_id_p2, NULL);
    pthread_join(thread_id_c1, NULL);
    // pthread_join(thread_id_c2, NULL);

    fclose(in_file);
    exit(0);
}
