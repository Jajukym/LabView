using System;
using System.IO.Ports;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

/**
 * CITS Console Test PROJECT
 *
 * Copyright @ 2020, CITS SOFTWARE, Co., Ltd. All Rights Reserved.
 */

namespace SampleTest
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            comboBox1.Items.AddRange(SerialPort.GetPortNames());
        }

        private void OnSelectChanged(object sender, EventArgs e)
        {
            var com = comboBox1.Text;
            Task.Run(() =>
            {
                UartManager.Get().OpenSeralPort(com);
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x2F, 0x0d });
                ASCIIEncoding encoding = new ASCIIEncoding();
                string consoleName = encoding.GetString(buffer).TrimEnd('\0');
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x3C, 0x03 });
                byte[] newByte = new byte[4];
                newByte[0] = buffer[2];
                newByte[1] = buffer[1];
                newByte[2] = buffer[0];
                int number = BitConverter.ToInt32(newByte, 0);
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x5B, 0x04 });
                int high = buffer[0] + buffer[1];
                int low = buffer[2] + buffer[3];
                string version = $"{high}.{low}";
                BeginInvoke(new MethodInvoker(() =>
                  {
                      lbConsoleName.Text = consoleName;
                      lbNumber.Text = Convert.ToString(number);
                      lbScanPart.Text = Convert.ToString(number); ;
                      lbFirmWare.Text = version;
                  }));
            });
        }

        private void OnClick(object sender, EventArgs e)
        {
            // compare serial number is start with part number
            if (sender == btnMatch)
            {
                if (tbSn.Text.Length <= lbScanPart.Text.Length)
                {
                    lbSnResult.Text = "sn is too short!";
                    return;
                }
                bool match = tbSn.Text.StartsWith(lbScanPart.Text);
                lbSnResult.Text = match ? "part number is match" : "part number not match";
            }

            //
            if (sender == btnPower)
            {
                GetPower();
            }
            if (sender == btnBle)
            {
                TestBle();
            }
            if (sender == btnPwm)
            {
                TestPwm();
            }
            if (sender == btnRes)
            {
                TestResistance();
            }
            if (sender == btnPulse)
            {
                TestPulse();
            }
            if (sender == btnFan)
            {
                TestFan();
            }
            if (sender == btnIncline)
            {
                TestIncline();
            }

            if (sender == btnOthers)
            {
                TestOther();
            }

            if (sender == btnCalibrate)
            {
                TestCalibrate();
            }
        }

        private void TestCalibrate()
        {
            Task.Run(() =>
            {
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x50, 0x01 });
                var feature = (buffer[0] & 0x08) > 0;
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x64, 0x01 });
                if (buffer[0] != 0x7)
                {
                    UartManager.Get().SendCommand(new byte[2] { 0x05, 0x02 });
                }
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x84, 0x01 });
                var status = (int)buffer[0];
                BeginInvoke(new MethodInvoker(() =>
                {
                    lbCalibrateFeature.Text = feature ? "has feature" : "no feature";
                    lbCalibrateStatus.Text = Convert.ToString(status);
                }));
                // while status == 4 (INCLINE_CALIBRATION_MODE_DONE) pass
            });
        }

        private void TestOther()
        {
            Task.Run(() =>
            {
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x51, 0x01 });
                var tvFeature = (buffer[0] & 0x80) > 0;
                var wahooFeature = (buffer[0] & 0x20) > 0;
                var csafeFeature = (buffer[0] & 0x10) > 0;

                buffer = UartManager.Get().SendCommand(new byte[2] { 0x50, 0x01 });
                var usbFeature = (buffer[0] & 0x01) > 0;
                BeginInvoke(new MethodInvoker(() =>
                {
                    lbTvFeature.Text = tvFeature ? "has feature" : " no feature";
                    lbUsbFeature.Text = usbFeature ? "has feature" : " no feature";
                    lbWahooFeature.Text = wahooFeature ? "has feature" : " no feature";
                    lbCsafeFeature.Text = csafeFeature ? "has feature" : " no feature";
                }));
            });
        }

        private void TestIncline()
        {
            var buffer = UartManager.Get().SendCommand(new byte[2] { 0x50, 0x01 });
            var feature = (buffer[0] & 0x08) > 0;
            buffer = UartManager.Get().SendCommand(new byte[2] { 0x80, 0x02 });
            var max = BitConverter.ToInt16(buffer, 0);
            buffer = UartManager.Get().SendCommand(new byte[2] { 0x82, 0x02 });
            var min = BitConverter.ToInt16(buffer, 0);
            buffer = UartManager.Get().SendCommand(new byte[2] { 0x7d, 0x02 });
            var incline = BitConverter.ToInt16(buffer, 0);
            BeginInvoke(new MethodInvoker(() =>
            {
                lbInclineFeature.Text = feature ? "has feature" : "no feature";
                lbIncline.Text = Convert.ToString(incline);
                lbMinincline.Text = Convert.ToString(min);
                lbMaxincline.Text = Convert.ToString(max);
            }));
            // i don't known how many quick incline should indicator operator to press
        }

        private void TestFan()
        {
            Task.Run(() =>
            {
                UartManager.Get().SendCommand(new byte[2] { 0x27, 0x02 });
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x50, 0x01 });
                var feature = (buffer[0] & 0x20) > 0;
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x6E, 0x02 });
                var current = BitConverter.ToInt16(buffer, 0);
                BeginInvoke(new MethodInvoker(() =>
                {
                    lbFanFeature.Text = feature ? "has Feature" : "no Feature";
                    lbFanCurrent.Text = Convert.ToString((float)current / 10);
                }));
            });
            // compare the current greater than a number?
        }

        private void GetPower()
        {
            Task.Run(() =>
            {
                UartManager.Get().SendCommand(new byte[2] { 0x27, 0x02 });
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x6C, 0x02 });
                var volage = BitConverter.ToInt16(buffer, 0);
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x6E, 0x02 });
                var current = BitConverter.ToInt16(buffer, 0);
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x70, 0x01 });
                var maxCurrent = (int)buffer[0];
                BeginInvoke(new MethodInvoker(() =>
                {
                    lbVoltage.Text = Convert.ToString((float)volage / 10);
                    lbCurrent.Text = Convert.ToString((float)current / 10);
                    lbCurrentMax.Text = Convert.ToString((float)maxCurrent / 10);
                }));
            });
        }

        private void TestBle()
        {
            Task.Run(() =>
            {
                UartManager.Get().SendCommand(new byte[2] { 0x27, 0x01 });
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x51, 0x01 });
                var hasFeature = (buffer[0] & 0x01) > 0;
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x02, 0x01 });
                var status = buffer[0];

                BeginInvoke(new MethodInvoker(() =>
                {
                    lbBleFeature.Text = hasFeature ? "has feature" : "no feature";
                    if (status == 0)
                        lbBleStatus.Text = "BLE is turned off";
                    else if (status == 1)
                        lbBleStatus.Text = "Initializing state";
                    else if (status == 2)
                        lbBleStatus.Text = "Peer device is connected";
                    else if (status == 3)
                        lbBleStatus.Text = "Advertising process";
                    else if (status == 4)
                        lbBleStatus.Text = "Scanning process";
                    else if (status == 5)
                        lbBleStatus.Text = "Connecting";
                    else if (status == 6)
                        lbBleStatus.Text = "Essentially idle state";
                }));
                // i don't  known how to judge the result,current larger than a number?
            });
        }

        private void TestPwm()
        {
            Task.Run(() =>
            {
                UartManager.Get().SendCommand(new byte[2] { 0x27, 0x00 });
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x86, 0x01 });
                var status = buffer[0];

                buffer = UartManager.Get().SendCommand(new byte[2] { 0x50, 0x01 });

                var feature = (buffer[0] & 0x04) > 0;

                buffer = UartManager.Get().SendCommand(new byte[2] { 0x9E, 0x01 });
                var rpm = buffer[0];

                buffer = UartManager.Get().SendCommand(new byte[2] { 0x89, 0x02 });
                var kpm = BitConverter.ToInt16(buffer, 0);

                buffer = UartManager.Get().SendCommand(new byte[2] { 0x90, 0x02 });
                var spm = BitConverter.ToInt16(buffer, 0);
                BeginInvoke(new MethodInvoker(() =>
                {
                    // status 0 is off ,send button start {0x05,0x04}
                    // display to operator
                    lbPwmFeature.Text = feature ? "has feature" : " no feature";
                    lbTachStatus.Text = Convert.ToString(status);
                    lbSpeed.Text = Convert.ToString((float)kpm / 10);
                    lbRpm.Text = Convert.ToString(rpm);
                    lbSpm.Text = Convert.ToString((float)spm / 10);
                }));
            });
        }

        private void TestResistance()
        {
            Task.Run(() =>
            {
                UartManager.Get().SendCommand(new byte[2] { 0x27, 0x00 });
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x51, 0x01 });
                var feature = (buffer[0] & 0x02) > 0;
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x93, 0x02 });
                var voltage = BitConverter.ToInt16(buffer, 0);
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x6E, 0x02 });
                var current = BitConverter.ToInt16(buffer, 0);
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x70, 0x01 });
                var maxCurrent = (int)buffer[0];
                BeginInvoke(new MethodInvoker(() =>
                {
                    lbResFeature.Text = feature ? "has feature" : "no feature";
                    lbResVoltage.Text = Convert.ToString((float)voltage / 10);
                    lbResCurrent.Text = Convert.ToString((float)current / 10);
                    lbResMaxCurrent.Text = Convert.ToString((float)maxCurrent / 10);
                    // i don't really known how to test quick resistance and increase decrease.
                }));
            });
        }

        private void TestPulse()
        {
            Task.Run(() =>
            {
                // this is necessary
                UartManager.Get().SendCommand(new byte[2] { 0x27, 0x01 });
                var buffer = UartManager.Get().SendCommand(new byte[2] { 0x51, 0x01 });
                var feature = (buffer[0] & 0x04) > 0;
                buffer = UartManager.Get().SendCommand(new byte[2] { 0x02, 0x01 });
                var status = (int)buffer[0];
                // while status is 0,send {0x0b,0x01}

                buffer = UartManager.Get().SendCommand(new byte[2] { 0x64, 0x01 });
                var display = (int)buffer[0];

                BeginInvoke(new MethodInvoker(() =>
                {
                    lbPulseFeature.Text = feature ? "has feature " : "no feature";
                    lbPulseStatus.Text = Convert.ToString(status);
                    lbDisplay.Text = Convert.ToString(display);
                }));
                // i don't how to judge the result,while status is connect auto pass?
            });
        }
    }
}