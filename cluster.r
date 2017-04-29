set.seed(1)
rstr <- function(n,k){   # vector of n random char(k) strings
  sapply(1:n,function(i){do.call(paste0,as.list(sample(letters,k,replace=T)))})
}

str<- c(paste0("aa",rstr(10,3)),paste0("bb",rstr(10,3)),paste0("cc",rstr(10,3)))
# Levenshtein Distance
d  <- adist(str)
rownames(d) <- str
hc <- hclust(as.dist(d))
plot(hc)
rect.hclust(hc,k=3)
df <- data.frame(str,cutree(hc,k=3))