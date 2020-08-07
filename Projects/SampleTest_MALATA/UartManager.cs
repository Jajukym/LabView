using System;
using System.IO.Ports;
using System.Threading;
using System.Threading.Tasks;

namespace SampleTest
{
    public class UartManager
    {
        private static UartManager _instance;
        private readonly static object _lock = new object();
        private readonly SerialPort _serialPort = new SerialPort();
        private readonly EventWaitHandle _eventWaitHandle = new EventWaitHandle(false, EventResetMode.AutoReset);
        private byte[] _buffer;

        private UartManager()
        {
        }

        public static UartManager Get()
        {
            if (_instance == null)
            {
                lock (_lock)
                {
                    if (_instance == null)
                    {
                        _instance = new UartManager();
                    }
                }
            }
            return _instance;
        }

        public void OpenSeralPort(string com)
        {
            try
            {
                if (!_serialPort.IsOpen)
                {
                    _serialPort.Close();
                }
                _serialPort.PortName = com;
                _serialPort.Parity = Parity.None;
                _serialPort.StopBits = StopBits.One;
                _serialPort.BaudRate = 9600;
                _serialPort.NewLine = "\r\n";
                _serialPort.Open();
                _serialPort.DataReceived += OnReceive;
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }

        private void OnReceive(object sender, SerialDataReceivedEventArgs e)
        {
            if (_serialPort.BytesToRead > 0)
            {
                _buffer = null;
                _buffer = new byte[_serialPort.BytesToRead];
                _serialPort.Read(_buffer, 0, _serialPort.BytesToRead);
                _eventWaitHandle.Set();
            }
        }

        public byte[] SendCommand(byte[] data)
        {
            if (data == null || data.Length <= 0) return null;
            Task task = new Task(() =>
            {
                _serialPort.Write(data, 0, data.Length);
                _eventWaitHandle.WaitOne();
            });
            task.Start(TaskScheduler.Current);
            task.Wait(1000);
            return _buffer;
        }
    }
}