#CODIGO ORIGINAL DE PLOTEO

#VISULIAZACION RADON (SIN DEPURAR)

def ticks_velocity(value,index):
    
    tick=angle2velocity(frame_rate,dx,value)
    
    return str('%.2f' % tick) #.2f significa float con 2 cifras decimales







flag_plot_individual_max = True 

    
#xticks_positions =  np.sort(list(set(np.round(np.linspace(theta2.min(),theta2.max(),19)*.1)/.1))).astype(int)
#xticks_labels = xticks_positions

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()


ax1.plot(thetas_max,maxpeaks[:,1] ,'ro')
lines = ax1.plot(theta2,median,theta2,mean)
l1,l2 = lines
plt.setp(l1,linewidth=8)
plt.setp(l2,linewidth=8)
#ax1.set_xticks(xticks_positions)
#ax1.set_xticklabels(xticks_labels)


majorLocator = MultipleLocator(10)
majorFormatter = FormatStrFormatter('%d')
minorLocator = AutoMinorLocator()
#minorLocator = MultipleLocator(2)

ax1.xaxis.set_major_locator(majorLocator)
ax1.xaxis.set_major_formatter(majorFormatter)
ax1.xaxis.set_minor_locator(minorLocator)
ax1.tick_params(which='both', width=2)
ax1.tick_params(which='major', length=7)
ax1.tick_params(which='minor', length=4, color='r')
x_ticks =  ax1.get_xticks()

ax1.set_xlim(theta_min,theta_max)
ax1.set_xlabel("Angulo de proyección (deg)")
ax1.set_ylabel('Varianza')
#ax1.grid()
ax1.xaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.yaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.xaxis.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)

#BANDERA PARA PLOTEAR VALOR MAXIMO DE MEAN
for xy in zip(thetas_max, mean_peak[:,1]):
    ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,thetas_max), xy=xy)



        
#        for xy in zip(thetas_max_k, maxpeaks_k[:,1]):
#            ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,thetas_max_k), xy=xy)
            

velocity_xticks_labels = angle2velocity(frame_rate,dx,ax1.get_xticks())

ax2.plot(theta2,Angular_density_2,'.',alpha=0.5)


ax2.xaxis.set_major_locator(majorLocator)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_locator(minorLocator)

ax2.tick_params(which='both', width=2)
ax2.tick_params(which='major', length=7)
ax2.tick_params(which='minor', length=4, color='r')


ax2.set_xlim(ax1.get_xlim())
#ax2.set_ylim(0,)
ax2.set_xlabel("Velocidad (m/s)")

if flag_plot_individual_max:
    ax1.plot(thetas_max_t,max_peaks_t ,'ro')
plt.show()



#%% #VISULIAZACION RADON (DEPURADA)


flag_plot_individual_max = True 
  

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()


lines = ax1.plot(theta2,median_filtered,theta2,mean_filtered)
l1,l2 = lines
plt.setp(l1,linewidth=8)
plt.setp(l2,linewidth=8)


majorLocator = MultipleLocator(10)
minorLocator = AutoMinorLocator()

ax1.xaxis.set_major_locator(majorLocator)
ax1.xaxis.set_minor_locator(minorLocator)
ax1.tick_params(which='both', width=2)
ax1.tick_params(which='major', length=7)
ax1.tick_params(which='minor', length=4, color='r')
x_ticks =  ax1.get_xticks()

ax1.set_xlim(theta_min,theta_max)
ax1.set_xlabel("Angulo de proyección (deg)")
ax1.set_ylabel('Varianza')
#ax1.grid()
ax1.xaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.yaxis.grid(b=True, which='major', color='k', linestyle='-', alpha = 0.5)
ax1.xaxis.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)

#BANDERA PARA PLOTEAR VALOR MAXIMO DE MEAN
ax1.plot(theta_mean_peak_filtered,mean_peak_filtered ,'go',markersize=15)
ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,theta_mean_peak_filtered),
              xy=[theta_mean_peak_filtered,mean_peak_filtered],fontsize=12)

#BANDERA PARA PLOTEAR VALOR MAXIMO DE MEDIAN
ax1.plot(theta_median_peak_filtered,median_peak_filtered ,'go',markersize=15)
ax1.annotate('Velocidad: %s m/s' % angle2velocity(frame_rate,dx,theta_median_peak_filtered), 
             xy=[theta_median_peak_filtered,median_peak_filtered],fontsize=12)
        

ax2.plot(theta2,Angular_density_filtered,'-',alpha=0.4)


ax2.xaxis.set_major_locator(majorLocator)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_formatter(ticker.FuncFormatter(ticks_velocity))
ax2.xaxis.set_minor_locator(minorLocator)

ax2.tick_params(which='both', width=2)
ax2.tick_params(which='major', length=7)
ax2.tick_params(which='minor', length=4, color='r')


ax2.set_xlim(ax1.get_xlim())
#ax2.set_ylim(0,)
ax2.set_xlabel("Velocidad (m/s)")

if flag_plot_individual_max:
    ax1.plot(thetas_max_t_filtered,max_peaks_t_filtered ,'ro')
    
plt.show()

#SELECCION DE CORRIENTE MEDIA



fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.hist(thetas_max_t_filtered,bins=25)






#%%
##VISUALIZACION Fourier

a,b = np.shape(Fourier_mean)


def ticks_x_fourier(value,index):
    
    tick=-frame_rate + (2*frame_rate/b)*value
    
    return str('%.2f' % tick)

def ticks_y_fourier(value,index):
    
    tick=dx + (2*frame_rate/b)*value
    
    return str('%.2f' % tick)

fig = plt.figure()
ax1 = fig.add_subplot(111)
plot_spec = ax1.imshow(np.log10(Fourier_mean_log10[0:int(a/2),::]),cmap=cm.viridis)
ax1.set_xlabel('Frequency [Hz')
ax1.set_ylabel('Wavenumbers [1/m]')
fig.colorbar(plot_spec,ax=ax1)

majorLocator = MultipleLocator(30)
minorLocator = AutoMinorLocator()
#minorLocator = MultipleLocator(2)
ax1.xaxis.set_major_locator(majorLocator)
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_x_fourier))
ax1.xaxis.set_minor_locator(minorLocator)
ax1.tick_params(which='both', width=2)
ax1.tick_params(which='major', length=7)
ax1.tick_params(which='minor', length=4, color='r')








# espectro con colorbar

fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
plot_ts = ax1.imshow(timestack,cmap='gray')
#fig.colorbar(plot_ts,ax=ax1)
plot_spec = ax2.imshow(mag,cmap='jet')
fig.colorbar(plot_spec,ax=ax2)