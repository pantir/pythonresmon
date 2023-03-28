import sys
import psutil
from psutil._common import bytes2human
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyqtgraph
from collections import deque
from itertools import repeat

import clr # https://stackoverflow.com/questions/3262603/accessing-cpu-temperature-in-python

clr.AddReference(r'./OpenHardwareMonitorLib')

from OpenHardwareMonitor import Hardware # https://github.com/openhardwaremonitor/openhardwaremonitor


class Panzerfaust(QMainWindow):
    def __init__(self):
        self.f = Hardware.Computer()
        self.f.MainboardEnabled = True
        self.f.GPUEnabled = True
        self.f.CPUEnabled = True
        self.f.Open()
        QMainWindow.__init__(self)
        self.ui = uic.loadUi("main.ui", self)
        self.tabWidget.tabBar().setDocumentMode(True)

        self.ui.nume_cpu.setText("Procesor: %s" %self.f.Hardware[1].Name)
        self.ui.nuclee_cpu.setText("Nuclee CPU: %d" %psutil.cpu_count(logical=False))
        self.ui.threads_cpu.setText("Fire de executie CPU: %d" %psutil.cpu_count(logical=True))
        self.ui.general_mobo.setText(self.f.Hardware[0].Name)
        self.ui.general_gpu.setText("GPU: %s" %" ".join(list(dict.fromkeys(self.f.Hardware[2].Name.split(" ")))))
        self.ui.general_cpu.setText("CPU: %s" %self.f.Hardware[1].Name)
        self.ui.general_ram.setText("RAM: %sB" %bytes2human(psutil.virtual_memory().total))

        self.deque_cpu = deque(repeat(0,60), maxlen=60) # Jarca Mihai
        self.deque_gpu = deque(repeat(0,60), maxlen=60)
        self.deque_ram = deque(repeat(0,60), maxlen=60)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update) # Jarca Mihai
        self.timer.setInterval(1000)
        self.timer.start()
        self.CPU_graph.getAxis('left').setTextPen(253, 184, 39)
        self.CPU_graph.getAxis('left').setPen(253, 184, 39)
        self.CPU_graph.getAxis('left').setLabel('CPU (%)')
        self.CPU_graph.getAxis('bottom').setTextPen(253, 184, 39)
        self.CPU_graph.getAxis('bottom').setPen(253, 184, 39)
        self.CPU_graph.getAxis('bottom').setLabel('timp (s)')
        self.CPU_graph.setBackground(background = (84, 37, 131))
        self.CPU_graph.setMouseEnabled(x = False, y = False)
        self.plotcpu = self.CPU_graph.plot(range(60), self.deque_cpu, brush = pyqtgraph.mkBrush(253, 184, 39, 150), fillLevel = 0, pen = pyqtgraph.mkPen(253, 184, 39))

        self.ui.GPU_title.setText("GPU: %s" %" ".join(list(dict.fromkeys(self.f.Hardware[2].Name.split(" ")))))
        self.GPU_graph.getAxis('left').setTextPen(253, 184, 39)
        self.GPU_graph.getAxis('left').setPen(253, 184, 39)
        self.GPU_graph.getAxis('left').setLabel('GPU (%)')
        self.GPU_graph.getAxis('bottom').setTextPen(253, 184, 39)
        self.GPU_graph.getAxis('bottom').setPen(253, 184, 39)
        self.GPU_graph.getAxis('bottom').setLabel('timp (s)')
        self.GPU_graph.setBackground(background = (84, 37, 131))
        self.GPU_graph.setMouseEnabled(x = False, y = False)
        self.plotgpu = self.GPU_graph.plot(range(60), self.deque_gpu, brush = pyqtgraph.mkBrush(253, 184, 39, 150), fillLevel = 0, pen = pyqtgraph.mkPen(253, 184, 39))

        self.RAM_graph.getAxis('left').setTextPen(253, 184, 39)
        self.RAM_graph.getAxis('left').setPen(253, 184, 39)
        self.RAM_graph.getAxis('left').setLabel('RAM (%)')
        self.RAM_graph.getAxis('bottom').setTextPen(253, 184, 39)
        self.RAM_graph.getAxis('bottom').setPen(253, 184, 39)
        self.RAM_graph.getAxis('bottom').setLabel('timp (s)')
        self.RAM_graph.setBackground(background = (84, 37, 131))
        self.RAM_graph.setMouseEnabled(x = False, y = False)
        self.plotram = self.RAM_graph.plot(range(60), self.deque_ram, brush = pyqtgraph.mkBrush(253, 184, 39, 150), fillLevel = 0, pen = pyqtgraph.mkPen(253, 184, 39))

    def updatecpu(self):
        self.f.Hardware[1].Update()
        for a in range(0, len(self.f.Hardware[1].Sensors)):
            if "/load/0" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.deque_cpu.append(int(self.f.Hardware[1].Sensors[a].get_Value()))
                self.ui.CPUtot.setText("Utilizare totala CPU: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
                self.updatepb(self.f.Hardware[1].Sensors[a].get_Value(), self.ui.circcpu, "rgba(253, 184, 39, 255)")
                self.ui.circ_cpu_per.setText("%d" %self.f.Hardware[1].Sensors[a].get_Value()+'%')
            elif "/load/1" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU0.setText("Utilizare nucleu 0: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/2" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU1.setText("Utilizare nucleu 1: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/3" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU2.setText("Utilizare nucleu 2: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/4" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU3.setText("Utilizare nucleu 3: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/5" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU4.setText("Utilizare nucleu 4: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/6" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU5.setText("Utilizare nucleu 5: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/7" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU6.setText("Utilizare nucleu 6: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/8" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU7.setText("Utilizare nucleu 7: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/9" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU8.setText("Utilizare nucleu 8: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/10" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU9.setText("Utilizare nucleu 9: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/11" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU10.setText("Utilizare nucleu 10: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")
            elif "/load/12" in str(self.f.Hardware[1].Sensors[a].Identifier):
                self.ui.CPU11.setText("Utilizare nucleu 11: %d" %int(self.f.Hardware[1].Sensors[a].get_Value()) + "%")

        self.plotcpu.setData(range(60), self.deque_cpu)

    def updategpu(self):
        self.f.Hardware[2].Update()
        for b in range(0, len(self.f.Hardware[2].Sensors)):
            if "/temperature" in str(self.f.Hardware[2].Sensors[b].Identifier):
                self.ui.GPU_temp.setText("Temperatura GPU: %d°C" %self.f.Hardware[2].Sensors[b].get_Value())
            if "/power" in str(self.f.Hardware[2].Sensors[b].Identifier):
                self.ui.GPU_pwr.setText("Putere consumata GPU: %.2fW" %self.f.Hardware[2].Sensors[b].get_Value())
            if "/fan" in str(self.f.Hardware[2].Sensors[b].Identifier):
                self.ui.GPU_fan.setText("Ventilator GPU: %dRPM" %self.f.Hardware[2].Sensors[b].get_Value())
            if "/load/0" in str(self.f.Hardware[2].Sensors[b].Identifier):
                self.deque_gpu.append(int(self.f.Hardware[2].Sensors[b].get_Value()))
                self.ui.GPU_usage.setText("Utilizare GPU: %d" %self.f.Hardware[2].Sensors[b].get_Value()+'%')
                self.ui.circ_gpu_per.setText("%d" %self.f.Hardware[2].Sensors[b].get_Value()+'%')
                self.updatepb(self.f.Hardware[2].Sensors[b].get_Value(), self.ui.circgpu, "rgba(253, 184, 39, 255)")

        self.plotgpu.setData(range(60), self.deque_gpu)

    def updateram(self):
        self.ui.RAM_total.setText("Memorie RAM totala: %sB" %bytes2human(psutil.virtual_memory().total))
        self.ui.RAM_free.setText("Memorie RAM libera: %sB" %bytes2human(psutil.virtual_memory().free))
        self.ui.RAM_used.setText("Memorie RAM folosita: %sB" %bytes2human(psutil.virtual_memory().used))

        self.deque_ram.append(psutil.virtual_memory().percent)
        self.ui.circ_RAM_per.setText("%s" %psutil.virtual_memory().percent + "%")
        self.ui.circ_RAM_per_2.setText("%s" %psutil.virtual_memory().percent + "%")
        self.plotram.setData(range(60), self.deque_ram)
        self.updatepb(psutil.virtual_memory().percent, self.ui.circRAM, "rgba(253, 184, 39, 255)")
        self.updatepb(psutil.virtual_memory().percent, self.ui.circRAM_2, "rgba(253, 184, 39, 255)")

    def updatepb(self, update, nume, color): #https://www.earthinversion.com/desktopapps/system-monitor-app-in-python/#install-libraries

        styleSheet = """
        QFrame{
        	border-radius: 110px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(253, 184, 39, 0), stop:{STOP_2} {COLOR});
        }
        """
        progress = (100 - update) / 100.0

        stop1 = str(progress - 0.001)
        stop2 = str(progress)

        if update == 100:
            stop1 = "1.000"
            stop2 = "1.000"

        newStylesheet = styleSheet.replace("{STOP_1}", stop1).replace("{STOP_2}", stop2).replace("{COLOR}", color)

        nume.setStyleSheet(newStylesheet)

    def update(self):
        self.updatecpu()
        self.updategpu()
        self.updateram()

app = QApplication(sys.argv)
window = Panzerfaust()
window.show()
sys.exit(app.exec_())