dfile = "anova.txt"
data = read.table(dfile, header=T)

# score
a.score = aov(score~(valence*block*gender*group)+
          Error(player/(valence*block))+(gender*group),
          data)
print('score')
print(summary(a.score))

# d-prime
a.dprime = aov(d_prime~(valence*block*gender*group)+
               Error(player/(valence*block))+(gender*group),
               data)
print('d prime')
print(summary(a.dprime))

# mean rt
a.meanrt = aov(mean_rt~(valence*block*gender*group)+
               Error(player/(valence*block))+(gender*group),
               data)
print('mean rt')
print(summary(a.meanrt))

# median rt
a.medrt = aov(med_rt~(valence*block*gender*group)+
              Error(player/(valence*block))+(gender*group),
              data)
print('median rt')
print(summary(a.medrt))

# motivation index
a.mi = aov(mot~(valence*block*gender*group)+
           Error(player/(valence*block))+(gender*group),
           data)
print('motivation index')
print(summary(a.mi))
