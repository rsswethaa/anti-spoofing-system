def pad_metrics(bona_fide_scores,attack_scores,threshold=.5):
    bona=[float(x) for x in bona_fide_scores]; attacks=[float(x) for x in attack_scores]
    if not bona or not attacks: raise ValueError('bona_fide_scores and attack_scores are required')
    threshold=float(threshold)
    if not 0<=threshold<=1: raise ValueError('threshold must be between 0 and 1')
    bpcer=sum(s<threshold for s in bona)/len(bona); apcer=sum(s>=threshold for s in attacks)/len(attacks); acer=(bpcer+apcer)/2
    return {'threshold':round(threshold,4),'APCER':round(apcer,4),'BPCER':round(bpcer,4),'ACER':round(acer,4),'bona_fide_samples':len(bona),'attack_samples':len(attacks)}
def threshold_sweep(bona,attacks,steps=21):
    rows=[pad_metrics(bona,attacks,i/(steps-1)) for i in range(steps)]; best=min(rows,key=lambda r:(r['ACER'],abs(r['APCER']-r['BPCER']))); return {'best_by_acer':best,'curve':rows}
