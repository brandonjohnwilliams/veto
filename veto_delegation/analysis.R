# List of CRAN packages
cran_packages <- c(
  "foreign", "plm", "stargazer", "patchwork", "ks", "lmtest",
  "dplyr", "stringr", "tidyr", "ggplot2", "svglite", "AER",
  "estimatr"
)

# Install missing CRAN packages
installed <- rownames(installed.packages())
for (pkg in cran_packages) {
  if (!pkg %in% installed) {
    install.packages(pkg)
  }
}

# Install gmoTree 
# Dependencies
install.packages(c(
  "data.table", "knitr", "openxlsx", "pander", 
  "plyr", "rlist", "rmarkdown"
))

# From a .tar.gz or .zip file:
install.packages("C:/Users/Brandon/Downloads/gmoTree_1.4.1.tar.gz", repos = NULL, type = "source")


# Load all packages
lapply(c("gmoTree", cran_packages), library, character.only = TRUE)

# Load in data
path <- "C:/Users/Brandon/Downloads/Data/Data"
  
rawData <- import_otree(path=path)
rawData<- delete_duplicate(rawData)
rawData <- make_ids(rawData)
rawData <- messy_time(rawData,combine = TRUE,info = TRUE)
rawData <- messy_chat(rawData,combine = TRUE,info = TRUE)
rawData <- delete_dropouts( rawData,final_apps = "payment", info = FALSE )
rawData <- assignv(rawData,  variable = "session.config.take_it_or_leave_it", newvar="offer.treat")
rawData <- assignv(rawData,  variable = "session.config.chat", newvar="chat.treat")


# Chats

match_chats_to_rounds <- function(Chats, Rounds) { 
  # Get chat end times by session and channel
  chat_endings <- Chats %>%
    group_by(session_code, channel) %>%
    summarise(
      chat_end_time = max(timestamp),
      participant_codes = list(unique(participant_code)),
      .groups = "drop"
    ) %>%
    tidyr::unnest(participant_codes, names_repair = "minimal") %>%
    rename(participant_code = participant_codes)
  
  # Join with rounds to find valid round completions after the chat
  matched <- chat_endings %>%
    left_join(Rounds, by = c("session_code", "participant_code"), relationship="many-to-many") %>%
    filter(chat_end_time <= epoch_time_completed+2) %>% #Allowing for rounding error
    group_by(session_code, channel, participant_code) %>%
    slice_min(epoch_time_completed, with_ties = FALSE) %>% # Closest round after chat
    ungroup()
  
  return(matched)
}

Chats <- rawData$Chats
Rounds <- subset(rawData$Time, app_name=="veto_delegation" & page_name=="Chat")
matched_chats <- as.data.frame(match_chats_to_rounds(Chats, Rounds))

chat_summary <- Chats %>%
  arrange(session_code, channel, timestamp,participant_code) %>%
  mutate(line = str_c(nickname, ": ", body)) %>%
  group_by(session_code, channel) %>%
  summarise(chat_text = str_c(line, collapse = "\n"), .groups = "drop") %>%
  as.data.frame()



round_mapping <- as.data.frame(unique(matched_chats[ ,c('session_code','channel', 'round_number' )]))

chat.df <- inner_join(chat_summary,round_mapping,by=c("session_code","channel"))

chat.p.df <- left_join(matched_chats[, c('session_code','channel','participant_code')], chat.df , by=c('session_code','channel') )

delegData <- rawData$veto_delegation
delegData$t <- delegData$subsession.round_number
delegData$session_code <- delegData$session.code
delegData$participant_code <- delegData$participant.code
delegData$round_number <- delegData$subsession.round_number
delegData$i <- delegData$participant_id
delegData$role <- delegData$player.role
delegData$minX <- delegData$group.minSlider
delegData$maxX <- delegData$group.maxSlider
delegData$y <- delegData$group.response
delegData$theta <- delegData$group.vetoer_bias
delegData$urn <- delegData$group.roundName
delegData$delegation <- ifelse(delegData$offer.treat, FALSE,TRUE)
delegData$chat <- ifelse(delegData$chat.treat, TRUE,FALSE)
delegData <- left_join(delegData, chat.p.df , by=c('session_code','participant_code','round_number') )
data <- delegData[, c('i','t','role','minX','maxX','y','theta','urn',"delegation","chat",'chat_text')]

subject_counts <- data %>%
  distinct(i, delegation, chat) %>%  # Ensure uniqueness by participant and treatment
  group_by(delegation, chat) %>%
  summarise(n_subjects = n(), .groups = 'drop')

as.data.frame(subject_counts)



chats.joined.df <- unique(subset(data, chat==TRUE )[ , c('delegation','t','urn','theta', 'chat_text','minX','maxX','y')])
chats.joined.df$mech <- ifelse(chats.joined.df$delegation, "Delegation",'TIOLI')
head(chats.joined.df)



export_chat_transcripts <- function(df, filepath) {
  # Open a connection
  con <- file(filepath, open = "wt")
  on.exit(close(con))
  df_sorted <- df %>% arrange(delegation, t)
  
  for (i in seq_len(nrow(df_sorted))) {
    row <- df_sorted[i, ]
    
    # Format the entry
    entry <- paste0(
      strrep("_", 50), "\n",
      sprintf("Round %d (%s), Urn=%s, theta=%d.", row$t, row$mech, row$urn, row$theta), "\n",
      strrep("-", 50), "\nChat log:\n",
      row$chat_text, "\n", strrep("-", 50), "\n",
      sprintf("\tSeller offer: %d-%d.\tBuyer choice: %d", row$minX, row$maxX, row$y), "\n",
      strrep("_", 50), "\n\n"
    )
    
    # Write to file
    writeLines(entry, con)
  }
  
  message("Export complete: ", filepath)
}
export_chat_transcripts(chats.joined.df, "chat_transcripts.txt")

#### DONE PRE-PROCESSING ####

# Plots of minimum offers

p1 <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==FALSE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Low (TioLi)")

p2<-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==FALSE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (TioLi)")

p3<-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==FALSE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (TioLi)")

p4 <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==TRUE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Low (Dele)")

p5<-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==TRUE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (Dele)")

p6<-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==TRUE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (Dele)")

DrawHist <- (p1 | p2 | p3)/(p4 | p5 | p6)
DrawHist



p1c <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==FALSE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Take-it-or-Leave-It: Low")

p2c <-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==FALSE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (TioLi)")

p3c <-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==FALSE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (TioLi)")

p4c <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==TRUE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Low (Dele)")

p5c <-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==TRUE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (Dele)")

p6c <-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==TRUE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (Dele)")

DrawHistc <- (p1c | p2c | p3c)/(p4c | p5c | p6c)
DrawHistc

##### Offers: Display plots #####

#### No Chat ####

# Theme for all plots

nice_blue <- "#4B9CD3"  # A clean, readable blue

nice_theme <- theme_classic(base_size = 12) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 13),
    axis.title = element_text(size = 11),
    axis.text = element_text(size = 10),
    axis.line = element_line(color = "black"),
    panel.grid.major.y = element_line(color = "gray90", size = 0.3),
    panel.grid.minor = element_blank()
  )

# Function to generate plots
make_offer_plot <- function(df, chat, delegation, urn_label) {
  df_plot <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == !!chat, delegation == !!delegation) %>%
    count(minX) %>%
    mutate(prop = n / sum(n))
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  y_label <- if (delegation) "Minimum Offer" else "Offer"
  title <- paste(label_main, ":", urn_label)
  
  ggplot(df_plot, aes(x = minX, y = prop)) +
    geom_col(fill = "#5DADE2", color = "black", width = 1) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.65)) +
    xlab(y_label) + ylab("Proportion") +
    ggtitle(title) + nice_theme
}

# Generate no-chat plots
p1 <- make_offer_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Low")
p2 <- make_offer_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Middle")
p3 <- make_offer_plot(data, chat = FALSE, delegation = FALSE, urn_label = "High")
p4 <- make_offer_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Low")
p5 <- make_offer_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Middle")
p6 <- make_offer_plot(data, chat = FALSE, delegation = TRUE, urn_label = "High")

DrawHist <- (p1 | p2 | p3) / (p4 | p5 | p6)
DrawHist

# Generate chat-enabled plots
p1c <- make_offer_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Low")
p2c <- make_offer_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Middle")
p3c <- make_offer_plot(data, chat = TRUE, delegation = FALSE, urn_label = "High")
p4c <- make_offer_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Low")
p5c <- make_offer_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Middle")
p6c <- make_offer_plot(data, chat = TRUE, delegation = TRUE, urn_label = "High")

DrawHistc <- (p1c | p2c | p3c) / (p4c | p5c | p6c)

# Display plots
DrawHist
DrawHistc

#### Accepted Offers ####

# Function for accepted offers (y)
make_accepted_plot <- function(df, chat, delegation, urn_label) {
  df_plot <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == !!chat, delegation == !!delegation) %>%
    count(y) %>%
    mutate(prop = n / sum(n))
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  y_label <- "Accepted Offer"
  title <- paste(label_main, ":", urn_label)
  
  ggplot(df_plot, aes(x = y, y = prop)) +
    geom_col(fill = "#117A65", color = "black", width = 1) +
    geom_vline(xintercept = 3, linetype = "dashed", color = "red") +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(y_label) + ylab("Proportion") +
    ggtitle(title) + nice_theme
}

# Generate plots: Accepted offers, no chat
a1 <- make_accepted_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Low")
a2 <- make_accepted_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Middle")
a3 <- make_accepted_plot(data, chat = FALSE, delegation = FALSE, urn_label = "High")
a4 <- make_accepted_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Low")
a5 <- make_accepted_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Middle")
a6 <- make_accepted_plot(data, chat = FALSE, delegation = TRUE, urn_label = "High")

DrawHistAccepted <- (a1 | a2 | a3) / (a4 | a5 | a6)

# Display
DrawHistAccepted

# Function for accepted offers (chat condition)
make_accepted_plot <- function(df, chat, delegation, urn_label) {
  df_plot <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == !!chat, delegation == !!delegation) %>%
    count(y) %>%
    mutate(prop = n / sum(n))
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  y_label <- "Accepted Offer"
  title <- paste(label_main, ":", urn_label)
  
  ggplot(df_plot, aes(x = y, y = prop)) +
    geom_col(fill = "#117A65", color = "black", width = 1) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(y_label) + ylab("Proportion") +
    ggtitle(title) + nice_theme
}

# Generate plots: Accepted offers, chat condition
a1c <- make_accepted_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Low")
a2c <- make_accepted_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Middle")
a3c <- make_accepted_plot(data, chat = TRUE, delegation = FALSE, urn_label = "High")
a4c <- make_accepted_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Low")
a5c <- make_accepted_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Middle")
a6c <- make_accepted_plot(data, chat = TRUE, delegation = TRUE, urn_label = "High")

DrawHistAcceptedChat <- (a1c | a2c | a3c) / (a4c | a5c | a6c)

# Display
DrawHistAcceptedChat



#### Overlay Plots ####

# Function for overlay histograms (no chat condition)
make_overlay_plot <- function(df, delegation, urn_label) {
  df_filtered <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == FALSE, delegation == !!delegation)
  
  df_offers <- df_filtered %>%
    count(minX) %>%
    mutate(prop = n / sum(n), type = "Offer", x = minX)
  
  df_accepts <- df_filtered %>%
    count(y) %>%
    mutate(prop = n / sum(n), type = "Accepted", x = y)
  
  df_plot <- bind_rows(df_offers, df_accepts)
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  title <- paste(label_main, ":", urn_label)
  x_label <- if (delegation) "Minimum Offer" else "Offer"
  
  ggplot(df_plot, aes(x = x, y = prop, fill = type)) +
    geom_col(position = "identity", width = 0.8, color = "black", alpha = 0.7) +
    scale_fill_manual(values = c("Offer" = "#b3b3f9", "Accepted" = "#117A65")) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(x_label) + ylab("Proportion") +
    ggtitle(title) +
    nice_theme +
    guides(fill = guide_legend(title = NULL))
}

# Create 6 overlay plots for no-chat condition
ov1 <- make_overlay_plot(data, delegation = FALSE, urn_label = "Low")
ov2 <- make_overlay_plot(data, delegation = FALSE, urn_label = "Middle")
ov3 <- make_overlay_plot(data, delegation = FALSE, urn_label = "High")
ov4 <- make_overlay_plot(data, delegation = TRUE, urn_label = "Low")
ov5 <- make_overlay_plot(data, delegation = TRUE, urn_label = "Middle")
ov6 <- make_overlay_plot(data, delegation = TRUE, urn_label = "High")

# Combine plots
DrawOverlayHist <- (ov1 | ov2 | ov3) / (ov4 | ov5 | ov6)

# Display
DrawOverlayHist


# Overlay plot function (chat condition)
make_overlay_plot <- function(df, delegation, urn_label) {
  df_filtered <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == TRUE, delegation == !!delegation)
  
  df_offers <- df_filtered %>%
    count(minX) %>%
    mutate(prop = n / sum(n), type = "Offer", x = minX)
  
  df_accepts <- df_filtered %>%
    count(y) %>%
    mutate(prop = n / sum(n), type = "Accepted", x = y)
  
  df_plot <- bind_rows(df_offers, df_accepts)
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  title <- paste(label_main, ":", urn_label)
  x_label <- if (delegation) "Minimum Offer" else "Offer"
  
  ggplot(df_plot, aes(x = x, y = prop, fill = type)) +
    geom_col(position = "identity", width = 0.8, color = "black", alpha = 0.7) +
    scale_fill_manual(values = c("Offer" = "#b3b3f9", "Accepted" = "#117A65")) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(x_label) + ylab("Proportion") +
    ggtitle(title) +
    nice_theme +
    guides(fill = guide_legend(title = NULL))
}

# Create 6 plots for chat condition
ov1c <- make_overlay_plot(data, delegation = FALSE, urn_label = "Low")
ov2c <- make_overlay_plot(data, delegation = FALSE, urn_label = "Middle")
ov3c <- make_overlay_plot(data, delegation = FALSE, urn_label = "High")
ov4c <- make_overlay_plot(data, delegation = TRUE, urn_label = "Low")
ov5c <- make_overlay_plot(data, delegation = TRUE, urn_label = "Middle")
ov6c <- make_overlay_plot(data, delegation = TRUE, urn_label = "High")

# Combine
DrawOverlayHistChat <- (ov1c | ov2c | ov3c) / (ov4c | ov5c | ov6c)

# Display
DrawOverlayHistChat

# Compare chat to no chat tioli

DrawOverlayChatTioli <- (ov1 | ov2 | ov3) / (ov1c | ov2c | ov3c)
DrawOverlayChatTioli

DrawOverlayChatDel <- (ov4 | ov5 | ov6) / (ov4c | ov5c | ov6c)
DrawOverlayChatDel

#### Cummulative offers in Delegation ####


# Helper function to compute proportions of values available in [minX:maxX]
get_value_availability <- function(df, urn_label, chat_cond) {
  df_filtered <- df %>%
    filter(
      delegation == TRUE,
      role == "Seller",
      t > 10,
      urn == urn_label,
      chat == chat_cond
    ) %>%
    select(i, t, minX, maxX)
  
  total_offers <- nrow(df_filtered)
  
  expanded <- df_filtered %>%
    rowwise() %>%
    mutate(offer_values = list(minX:maxX)) %>%
    unnest(offer_values) %>%
    ungroup() %>%
    distinct(i, t, offer_values) %>%
    count(offer_values) %>%
    mutate(proportion = n / total_offers)
  
  # Fill missing values from 0 to 9 with 0
  full <- tibble(offer_values = 0:9) %>%
    left_join(expanded, by = "offer_values") %>%
    mutate(proportion = replace_na(proportion, 0))
  
  return(full)
}

# Generate 6 datasets
plot_data <- list(
  low_nochat  = get_value_availability(data, "Low", FALSE),
  mid_nochat  = get_value_availability(data, "Middle", FALSE),
  high_nochat = get_value_availability(data, "High", FALSE),
  low_chat    = get_value_availability(data, "Low", TRUE),
  mid_chat    = get_value_availability(data, "Middle", TRUE),
  high_chat   = get_value_availability(data, "High", TRUE)
)

# Plotting function
make_availability_plot <- function(df, title) {
  ggplot(df, aes(x = offer_values, y = proportion)) +
    geom_col(fill = "#117A65", color = "black", width = 0.8) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 1)) +
    xlab("Value Offered") + ylab("Proportion of Offers Including Value") +
    ggtitle(title) +
    nice_theme
}

# Generate plots
p1 <- make_availability_plot(plot_data$low_nochat, "Low Urn (No Chat)")
p2 <- make_availability_plot(plot_data$mid_nochat, "Middle Urn (No Chat)")
p3 <- make_availability_plot(plot_data$high_nochat, "High Urn (No Chat)")
p4 <- make_availability_plot(plot_data$low_chat, "Low Urn (Chat)")
p5 <- make_availability_plot(plot_data$mid_chat, "Middle Urn (Chat)")
p6 <- make_availability_plot(plot_data$high_chat, "High Urn (Chat)")

# Combine with patchwork
DelegationValueAvailability <- (p1 | p2 | p3) / (p4 | p5 | p6)

# Show all
DelegationValueAvailability

#### Delegation: Accepted offers out of all available #### 

# Helper function to compute proportions of availability and acceptance
get_overlay_data <- function(df, urn_label, chat_cond) {
  df_filtered <- df %>%
    filter(
      delegation == TRUE,
      role == "Seller",
      t > 10,
      urn == urn_label,
      chat == chat_cond
    ) %>%
    select(i, t, minX, maxX, y)
  
  total_offers <- nrow(df_filtered)
  
  # Expand [minX:maxX] values
  available <- df_filtered %>%
    rowwise() %>%
    mutate(offer_values = list(minX:maxX)) %>%
    unnest(offer_values) %>%
    ungroup() %>%
    distinct(i, t, offer_values) %>%
    count(offer_values) %>%
    mutate(avail_prop = n / total_offers)
  
  # Accepted offers (y)
  accepted <- df_filtered %>%
    count(y) %>%
    rename(offer_values = y, accepted_n = n) %>%
    mutate(acc_prop = accepted_n / total_offers)
  
  # Merge and fill missing values
  full <- tibble(offer_values = 0:9) %>%
    left_join(available, by = "offer_values") %>%
    left_join(accepted, by = "offer_values") %>%
    mutate(
      avail_prop = replace_na(avail_prop, 0),
      acc_prop   = replace_na(acc_prop, 0)
    )
  
  return(full)
}

# Plot function: gray bar for availability, green bar for accepted
make_overlay_bar_plot <- function(df, title) {
  ggplot(df, aes(x = offer_values)) +
    geom_col(aes(y = avail_prop), fill = "#D5D8DC", color = "black", width = 0.8) +
    geom_col(aes(y = acc_prop), fill = "#117A65", width = 0.5) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 1)) +
    xlab("Value") + ylab("Proportion") +
    ggtitle(title) +
    nice_theme
}

# Regenerate overlay plots
p1g <- make_overlay_bar_plot(overlay_data$low_nochat, "Low Urn (No Chat)")
p2g <- make_overlay_bar_plot(overlay_data$mid_nochat, "Middle Urn (No Chat)")
p3g <- make_overlay_bar_plot(overlay_data$high_nochat, "High Urn (No Chat)")
p4g <- make_overlay_bar_plot(overlay_data$low_chat, "Low Urn (Chat)")
p5g <- make_overlay_bar_plot(overlay_data$mid_chat, "Middle Urn (Chat)")
p6g <- make_overlay_bar_plot(overlay_data$high_chat, "High Urn (Chat)")

# Combine with patchwork
OverlayBarCharts <- (p1g | p2g | p3g) / (p4g | p5g | p6g)

# Show
OverlayBarCharts

#### Seller Payoffs ####



seller_data <- data %>%
  filter(role == "Seller" & t>5 ) %>%
  group_by(delegation, chat, urn) %>%
  summarise(
    n = n(),
    avg.widgets = round(mean(y),3),
    ,.groups = 'drop') %>%
  ungroup()

seller_data$Mech <- ifelse(seller_data$delegation, "Delegation", "TIOLI")
seller_data$Comm <- ifelse(seller_data$chat, "Chat", "NoChat")

seller_data <- pivot_wider(seller_data[, c("Mech","Comm",'urn','avg.widgets')], names_from = urn, values_from = avg.widgets)

seller_data[, c("Mech","Comm",'Low','Middle','High')]

late.seller <- subset(data,t>5 & role == "Seller")
late.seller$dist<-as.factor(late.seller$urn)

y.out <- lm_robust( y ~  dist*delegation*chat, data= late.seller, cluster=i)

summary(y.out)


new.data <- expand.grid(
  dist = as.factor(c("Low", "Middle", "High")),
  delegation = c(TRUE, FALSE),
  chat = c(TRUE, FALSE)
)

prediction <- prediction(y.out, data = new.data)
prediction


#### Breakdown Graphs ####