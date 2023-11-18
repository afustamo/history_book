library(shiny)
library(ggplot2)

# Initialize an empty data frame to store character information
characters <- data.frame(
  name = character(),
  date_of_birth = character(),
  date_of_death = character(),
  stringsAsFactors = FALSE
)

# Define UI
ui <- fluidPage(
  titlePanel("Historical Characters Game"),
  sidebarLayout(
    sidebarPanel(
      numericInput("choice", "Enter your choice:", min = 0, max = 5, value = 0),
      actionButton("submit", "Submit")
    ),
    mainPanel(
      textOutput("output"),
      plotOutput("map")
    )
  )
)

# Define server logic
server <- function(input, output) {
  observeEvent(input$submit, {
    switch(input$choice,
           "1" = add_character(),
           "2" = modify_character(),
           "3" = display_character_info(),
           "4" = print(display_map()),
           "5" = export_map(),
           "0" = {
             cat("Closing the game. Goodbye!\n")
             stopApp()  # Stop the Shiny app
           },
           cat("Invalid choice. Please enter a valid option.\n")
    )
  })
  
  # Function to add a new character
  add_character <- function() {
    name <- isolate(input$name)
    birth_date <- isolate(input$birth_date)
    death_date <- isolate(input$death_date)
    
    # Add the new character to the data frame
    new_character <- data.frame(
      name = name,
      date_of_birth = birth_date,
      date_of_death = ifelse(death_date == "", NA, death_date),
      stringsAsFactors = FALSE
    )
    characters <<- rbind(characters, new_character)
    cat("Character added successfully!\n")
  }
  
  
  # Function to modify an existing character
  modify_character <- function() {
    cat("Enter the name of the character to modify: ")
    char_name <- readline()
    
    # Check if the character exists
    if (char_name %in% characters$name) {
      cat("Enter the new details for the character:\n")
      birth_date <- readline(prompt = "New Date of Birth (YYYY/MM/DD): ")
      death_date <- readline(prompt = "New Date of Death (Leave blank if alive): ")
      
      # Update the character in the data frame
      characters[characters$name == char_name, "date_of_birth"] <- birth_date
      characters[characters$name == char_name, "date_of_death"] <- ifelse(death_date == "", NA, death_date)
      cat("Character modified successfully!\n")
    } else {
      cat("Character not found.\n")
    }
  }
  
  # Function to display character information
  display_character_info <- function() {
    cat("Enter the name of the character to display information: ")
    char_name <- readline()
    
    # Check if the character exists
    if (char_name %in% characters$name) {
      cat("Character Information:\n")
      print(characters[characters$name == char_name, ])
    } else {
      cat("Character not found.\n")
    }
  }
  
  # Function to display the map
  display_map <- function() {
    ch2 <- characters
    ch2$date_of_death <- as.Date(ch2$date_of_death)
    ch2$date_of_death[is.na(ch2$date_of_death)]<-as.Date(Sys.Date())
    ggmap <- ggplot(ch2) +
      geom_segment(
        aes(
          y = name,
          yend = name,
          x = as.Date(date_of_birth),
          xend = as.Date(date_of_death),
          color = name  # Use the name for coloring
        ),
        linewidth = 3,  # Adjust the width of the segment
        show.legend = FALSE  # Hide the legend for geom_segment
      ) +
      geom_text(
        aes(
          y = name,
          x = as.Date((as.numeric(as.Date(date_of_birth)) + as.numeric(as.Date(date_of_death))) / 2),
          label = name
        ),
        vjust = 0,
        size = 3,  # Adjust the size of the text
        show.legend = FALSE  # Hide the legend for geom_text
      ) +
      scale_x_date(limits = c(as.Date("1800/1/1"), Sys.Date())) +
      scale_color_brewer(palette = "Pastel1") +  # Use a light color palette
      ggtitle("Historical Characters Map")
    rm(ch2)
    return(ggmap)
  }
  
  
  # Function to export the map (not implemented)
  export_map <- function() {
    cat("Exporting the map (to be implemented).\n")
  }
  
}

# Run the application
shinyApp(ui = ui, server = server)