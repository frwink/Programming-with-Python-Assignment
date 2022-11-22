import matplotlib.pyplot as plt

class XYPlotter:
    """
    This class contains a method that is responsible for plotting data in the form x,y1,y2,y3,...yn as line or scatter graph
    You can speficy which columns columnList={yi,yj,...} you want to plot from data
    """
    def plotXYData(self, data, columnList, plot_type='plot', label = ''):
        X = [row[0] for row in data] 
        for idx in columnList:
            Y = [row[idx] for row in data]
            if plot_type=='plot':
                plt.plot(X,Y, label = label)
            elif plot_type=='scatter':
                plt.scatter(X,Y,label=label)
            else:
                raise Exception(f'Invalid plot type') 