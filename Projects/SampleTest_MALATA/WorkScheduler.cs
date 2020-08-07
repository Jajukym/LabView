using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace icon
{
    internal class WorkScheduler : TaskScheduler
    {
        public static new TaskScheduler Current { get; } = new WorkScheduler();

        public static new TaskScheduler Default { get; } = Current;
        private readonly BlockingCollection<Task> _queue = new BlockingCollection<Task>();

        private WorkScheduler()
        {
            Thread thread = new Thread(Run);
            //设为为后台线程，当主线程结束时线程自动结束
            thread.IsBackground = true;
            thread.Start();
        }

        private void Run()
        {
            Task t;
            while (_queue.TryTake(out t, Timeout.Infinite))
            {
                //在当前线程执行Task
                TryExecuteTask(t);
            }
        }

        protected override IEnumerable<Task> GetScheduledTasks()
        {
            return _queue;
        }

        protected override void QueueTask(Task task)
        {
            //将Task加入到队列中
            _queue.Add(task);
        }

        //当执行该函数时，程序正在尝试以同步的方式执行Task代码
        protected override bool TryExecuteTaskInline(Task task, bool taskWasPreviouslyQueued)
        {
            return false;
        }
    }
}