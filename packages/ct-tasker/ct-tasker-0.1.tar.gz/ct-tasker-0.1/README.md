# tasker

## Creative Tool Test  

## Easy Job Scheduler 

We want you to write a simple program that is able to execute a task which may or may not have dependencies on other tasks to be executed before. 

A task is executed at the command line and is defined in a regular text ASCII file as follows: 

- the name of the task  
- the command of the task  
- a comma-separated list of task dependencies  

For Example: 

A.task: 

> A  
echo 'I am task A'`

B.task: 

> B  
echo 'I am task B' 

C.task: 

> C  
echo 'I am task C'  
A, B 

The program is invoked to execute the task(s) thus: 

> ./job_scheduler <task_to_be_done>  [TASK_FILE_0, ...] 

where first argument <task_to_be_done> it is the name of the task to be run and the other argument are file paths of the task definition files. 

 

So, with the given task sample files, you might run for example: 

> ./job_scheduler A A.task B.task C.task  
I am A 

> ./job_scheduler C A.task B.task C.task  
I am A  
I am B  
I am C 

> ./job_scheduler B A.task C.task  
Error! 

### Delivery: 

You are expected to deliver your solution in a gitlab, github or bitbucket repository accessible to us. The commit history of the repo will form part of our analysis of your work. 

### General Notes: 

This exercise should not take you more than 5 hours. 

You are expected to write testable and documented code where you explain the design and the implementation. 

The C++ code and its compilation process should be as portable as possible. 

 

Specifically:  

you are free to adopt data structure and algorithms you see fit the purpose. 

you can use the C++ standand level you prefer (C++11, C++14, C++17) 

you can make use of std::system  in <cstdlib> for executing the command of a task or you are free to use other framework. 

you are free to use external libraries as far as those are portable, you understand clearly what they do and you are able to argument the reason of why you choose them before other approaches. 

 

In your interview we will discuss your solution, its corner cases, possible pitfall, test case that you did not handle, and any sort of future improvements that you or us see as valid or important. 

 

Good Luck! 

 

 

 