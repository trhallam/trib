"""XChartTools

This file contains functions which help build charts using QtCharts

"""

from PyQt5.QtChart import (
    QBarSeries, QBarSet, QBarCategoryAxis, QHorizontalBarSeries,
    QBoxPlotSeries, QBoxSet,
    QCandlestickSeries, QCandlestickSet,
    QScatterSeries, QLineSeries)

from itertools import zip_longest

# build a bar chart from a dictionary of values

def XDictSet(data_dict, chart_type='bar', key_order=None):
    known_chart_types = ['bar', 'hbar', 'box', 'candlestick']

    if chart_type in known_chart_types:

        if key_order == None:
            key_order = data_dict.keys()

        def dictloop(data, ko, QSeries, QSet):
            for key in ko:
                print(key)
                set = QSet(key)
                for item in data[key]:
                    try:
                        set << float(item)
                    except (ValueError, TypeError):
                        set << 0.0
                QSeries.append(set)
            return QSeries

        if chart_type == 'bar':
            series = dictloop(data_dict, key_order, QBarSeries(), QBarSet)
        if chart_type == 'hbar':
            series = dictloop(data_dict, key_order, QHorizontalBarSeries(), QBarSet)
        elif chart_type == 'box':
            series = dictloop(data_dict, key_order, QBoxPlotSeries(), QBoxSet)
        elif chart_type == 'candlestick':
            series = dictloop(data_dict, key_order, QCandlestickSeries(), QCandlestickSet)
    else:
        raise ValueError('chart_type is unknown')
        pass
    return series


def XLineSeries(data_dict, key_order=None, xkey = None, openGL=False):
    if key_order == None:
        key_order = data_dict.keys()

    series = []
    if xkey == None:
        xkey = list(key_order)[0]
    for key in key_order-xkey:
        set = QLineSeries(); set.setName(key)
        if openGL:
            set.setUseOpenGL(True)        
        for i, (itemx, itemy) in enumerate(zip_longest(data_dict[xkey],data_dict[key])):
            set.append(itemx, itemy)

        series.append(set)
    return series

def XScatterSeries(data_dict, key_order = None, xkey = None, openGL=False):
    '''
    the first dict in the key_order will be used as the x-axis
    '''
    if key_order==None:
        key_order = data_dict.keys()

    series = []
    if xkey == None:
        xkey = list(key_order)[0]
    for key in key_order-xkey:
        set = QScatterSeries(); set.setName(key)
        if openGL:
            set.setUseOpenGL(True)        
        for i, (itemx, itemy) in enumerate(zip_longest(data_dict[xkey],data_dict[key])):
            set.append(itemx, itemy)

        series.append(set)
    return series

def main():
    import sys
    from PyQt5.QtChart import QChart, QChartView
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    data = dict()
    data["Jane"] = [1, 2, 3, 4, 5, 6]
    # data["John"] = [5, 0, 0, 4, 0, 7]
    # data["Axel"] = [3, 5, 6, 7, 2, 2]
    # data["Mary"] = [3, 5, 7, 2, 3, 5]
    # data["Tony"] = [3, 0, 9, 3 ,1, 2]

    # series=XDictSet(data, key_order=['Jane', 'John', 'Axel', 'Mary', 'Tony'])
    series = XDictSet(data)
    lineseries = XLineSeries(data);
    print(lineseries)

    chart = QChart()
    chart.addSeries(series)
    chart.addSeries(lineseries[0])
    chart.setTitle("Simple horizontal barchart example")
    chart.setAnimationOptions(QChart.SeriesAnimations)

    categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    axis = QBarCategoryAxis()
    axis.append(categories)
    chart.createDefaultAxes()
    chart.setAxisX(axis, series)

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
