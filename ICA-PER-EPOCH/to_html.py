pids = range(1001, 1022)
conds = ['PV0', 'PV1', 'WM0', 'WM1']

for p, pid in enumerate(pids):

    for c, cond in enumerate(conds):

        for trial in range(48):

            # open the output file
            fid = open("%d_%s_%d.html" % (pid, cond, trial), 'w')
            
            # define the image file
            imfile = "%d_%s_%d_epo-ica.png" % (pid, cond, trial)
            
            # define the next file
            if trial < 47:
                nxt = "%d_%s_%d.html" % (pid, cond, trial+1)
            elif c < 3:
                nxt = "%d_%s_%d.html" % (pid, conds[c+1], 0)
            elif p < 20:
                nxt = "%d_%s_%d.html" % (pids[p+1], 'PV0', 0)
            else:
                nxt = "1001_PV0_0.html"
           
            # define the previous file
            if trial > 0:
                prv = "%d_%s_%d.html" % (pid, cond, trial-1)
            elif c > 0:
                prv = "%d_%s_%d.html" % (pid, conds[c-1], 47)
            elif p > 0:
                prv = "%d_%s_%d.html" % (pids[p-1], 'WM1', 47)
            else:
                prv = "1021_WM1_47.html"           
 
            # write to the output file
            fid.write('<!DOCTYPE html>\n<html>\n<body>\n' + 
                      '<img src="%s" ' % imfile + 
                      'style="width:1500px;height:750px;">\n' +
                      '<div align="left">' +
                      '<a href="%s">Prev</a></div>\n' % prv +
                      '<div align="right">' +
                      '<a href="%s">Next</a></div>\n' % nxt +
                      '</body>\n</html>')

            # close the output file
            fid.close()
