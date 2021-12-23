'''
Funciones importantes que voy a usar:

sorter.getSimilarTemplates(17)
sorter.getClosestsTemplates(10)
sorter.subdivideClusters(7, 2) cual divido y en cuantos
sorter.mergeClusters(14, [26, 28]) a donde lo mando, vector: cuales mergeo
sorter.plotClusteredEvents(clust_list= [0,1], step = 1) este te muestra la medicion con los clusters hecho puntito
sorter.hideClusters(4) te ignora ese cluster
sorter.hideBadEvents(clust_list=[lista])
generatePrediction(self, before, after, store_prediction=True, peak_idxs=None) independiente
sorter.clusteringPrediction() dependiente
sum(sorter.train_clusters==n`cluster ej 6)
sorter.secondaryPeeling(vect_len=5, threshold=20, min_dist=100, store_mid_steps=False)
sorter.peaks_idxs
sorter.train_clusters
sorter.final_spike_dict
plotCompleteDetection


clusters_unicos=np.unique(sorter.train_clusters)
for i in range(len(clusters_unicos)):
    ct=np.count_nonzero(clusters_unicos[i] == sorter.train_clusters)
    print(clusters_unicos[i], ct)


sorter.plotCompleteDetection(legend=True)
spike_freqs = burstUtils.getInstFreq(sorter.time, sorter.final_spike_dict, sorter.sample_freq)

burstUtils.plotFreq(burst_object.spike_freq_dict, burst_object.color_dict, template_dict=burst_object.template_dict,
                                  scatter_plot=True, outlier_thres=3.5, ms=2)

'''