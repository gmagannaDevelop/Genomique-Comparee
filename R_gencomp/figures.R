
library(tidyverse)

c.genome.sizes <- 
  read_csv("../Data/Statistics/core_genomes_diversity.csv") %>% 
    select(n_strains, core_genome_size)

summarise.times <- function(
  df, time_var = exec_time, grouping_var = threads
){
  time_var <- enquo(time_var)
  grouping_var <- enquo(grouping_var)
  time_name <- as_label(time_var)
  
  df %>%
    mutate( !!time_name := round({{time_var}}, 2)) %>% 
    group_by(!!grouping_var) %>% 
    summarise(
      mean_time := round(mean(!!time_var), 2), 
      sd := round(sd(!!time_var),2),
      best := min(!!time_var),
      worst := max(!!time_var)
    )
}

plot_times <- function(
  df, x_var, y_var, title
){
  x_var <- enquo(x_var)
  y_var <- enquo(y_var)
  
  df %>% 
    ggplot(mapping = aes(x=!!x_var, y=!!y_var)) +
    geom_boxplot(aes(group=!!x_var, y=!!y_var)) + 
    geom_point(alpha=0.3) +
    geom_smooth() + 
    ggtitle(title)
}

c.genome.sizes %>% plot_times(n_strains, core_genome_size, "Core genome size ~ number of strains (20 random samples each)")
