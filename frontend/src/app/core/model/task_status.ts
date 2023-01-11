export interface TaskStatus {
    task_state: string
    task_status: string
    task_status_id: TaskStatuses
    task_id: string
}


export enum TaskStatuses {
    NotCreated = 0,
    Started = 1,
    Pending = 2,
    Ended = 3
}

export interface UpdateSentimentsTasks {
    tasks: { [key: string]: TaskStatus }
}