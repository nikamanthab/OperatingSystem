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
int counter = 0;

void* print_buffer(char b[10][100]){
    printf("\n------------\n");
    for(int i=0;i<10;i++){
        printf("%s", b[i]);
    }
    printf("\n------------\n");

}

int write_to_buffer(head_ptr){
    if ((read_line = getline(&line, &len, in_file)) != -1) {
        printf("Retrieved line of length %zu:\n", read_line);
        printf("%s", line);
    }
    printf("line:%s", line);
    strcpy(buffer[head_ptr], line);
    strcpy(line, "");
    print_buffer(buffer);
    return read_line;
}

void *read_from_buffer(tail_ptr){
    char* string = buffer[tail_ptr];
    fprintf(out_file, "%s", string);
    fflush(out_file);
    return NULL;
}

void *producer(void *vargp){
    int repeat = 1;
    while(repeat > 0){
        sem_wait(&sem_p);
        pthread_mutex_lock(&mutex);
        repeat = write_to_buffer(head_ptr);
        if(repeat > 0){
        head_ptr = (head_ptr+1)%N;
        }
        pthread_mutex_unlock(&mutex);
        sem_post(&sem_c);
    }
    return NULL;
}
void *consumer(void *vargp){
    while(counter<60){
        printf("head_ptr: %d-> tail_ptr: %d\n",head_ptr,tail_ptr);
        sem_wait(&sem_c);
        pthread_mutex_lock(&mutex);
        counter+=1;

        read_from_buffer(tail_ptr);
        tail_ptr = (tail_ptr+1)%N;
        pthread_mutex_unlock(&mutex);
        sem_post(&sem_p);
    }
    return NULL;
}

void main(){
    in_file = fopen("./input.txt", "r");
    out_file = fopen("./output.txt", "w");
    sem_init(&sem_p, pshared_p, N);
    sem_init(&sem_c, pshared_c, N);
    count = 0;
    pthread_create(&thread_id_p1, NULL, producer, NULL);
    pthread_create(&thread_id_p2, NULL, producer, NULL);
    pthread_create(&thread_id_c1, NULL, consumer, NULL);
    pthread_create(&thread_id_c2, NULL, consumer, NULL);

    pthread_join(thread_id_p1, NULL);
    pthread_join(thread_id_p2, NULL);
    pthread_join(thread_id_c1, NULL);
    pthread_join(thread_id_c2, NULL);

    fclose(in_file);
    fclose(out_file);
    exit(0);
}
