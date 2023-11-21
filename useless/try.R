setwd("h")

df <-
  data.frame(
    name = c("a", "b"),
    date_of_birth = c("1995/9/26", "1993/2/4"),
    date_of_death = NA
  )
df <-
  data.frame(
    name = c("a", "b"),
    date_of_birth = c("1895/9/26", "1893/2/4"),
    date_of_death = c("1995/9/26", "1993/2/4")
  )

library(ggplot2)
ggplot(df) +
  geom_segment(aes(
    y = name,
    yend = name,
    x = as.Date(date_of_birth),
    xend = as.Date(date_of_death)
  ),linewidth=2) +
  scale_x_date(limits = c(as.Date("1000/1/1"), Sys.Date()))

while (TRUE) {
    cat("Seleziona un opzione:\n")
    cat("1: Aggiungere un personaggio\n")
    cat("2: Modificare un personaggio esistente\n")
    cat("3: Visualizzare la scheda di un personaggio\n")
    cat("4: Visualizza la mappa\n")
    cat("4: Esporta la mappa\n")
    cat("0: Chiudi\n")
  }
