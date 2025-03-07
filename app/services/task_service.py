from sqlmodel import Session, select
from app.models.task_tracking import TaskTracking
from app.models.work_assignment import WorkAssignment


def get_dependent_tasks(session: Session, task_id: int):
    """Fetch all tasks that depend on the given task."""
    return session.exec(
        select(TaskTracking)
        .where(TaskTracking.work_assignment_id == task_id)
        ).all()


def adjust_task_priority(session: Session, task_id: int):
    """Adjust priorities of dependent tasks when a task is delayed."""
    processed_tasks = set()
    queue = [task_id]

    while queue:
        current_task_id = queue.pop(0)
        if current_task_id in processed_tasks:
            continue
        processed_tasks.add(current_task_id)

        # Fetch the current task
        current_task = session.get(WorkAssignment, current_task_id)
        if not current_task:
            continue

        # Fetch dependent tasks
        dependent_tasks = get_dependent_tasks(session, current_task_id)
        for task in dependent_tasks:
            dependent_task = session.get(WorkAssignment, task.id)
            if not dependent_task:
                continue

            # Update dependent task's priority
            if dependent_task.order <= current_task.order:
                dependent_task.order = current_task.order + 1  # Push it further in sequence
                session.add(dependent_task)
                queue.append(dependent_task.id)

    session.commit()
