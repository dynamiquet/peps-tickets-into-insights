function mergeTDXData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ticketSheet = ss.getSheetByName("TDX Peps Tickets Report January");
  var taskSheet = ss.getSheetByName("TDX Peps Task Report January 2");
  var mergedSheet = ss.getSheetByName("Merged Report") || ss.insertSheet("Merged Report");

  mergedSheet.clear(); // Clear old data

  var ticketData = ticketSheet.getDataRange().getValues();
  var taskData = taskSheet.getDataRange().getValues();

  var mergedData = [];
  var ticketMap = {};

  // Create a header row
  mergedData.push([
    "Ticket ID", "Requestor", "Title", "Acct/Dept", "Service", "Peps Location", "Other Location",
    "Peps Event Types", "Created", "Status", "PEPS Videotaping Info", "Peps Event Type Other",
    "PEPS Events Projection", "PEPS Events Proj. Device", "PEPS Events Media Present1",
    "Resolved Date", "Type", "Responsibility", "Resp Group",
    "Task IDs", "Task Titles", "Task Created Dates", "Task Due Dates", "Event Start Times", "Task Resp Groups", "Task Responsibilities"
  ]);

  // Store ticket data in a map using Ticket ID as key
  for (var i = 1; i < ticketData.length; i++) {
    var ticketID = ticketData[i][2]; // Assuming Ticket ID is in column C (index 2)

    if (!ticketMap[ticketID]) {
      ticketMap[ticketID] = {
        ticketDetails: ticketData[i].slice(0, 19), // Store ticket information
        tasks: {
          ids: [],
          titles: [],
          createdDates: [],
          dueDates: [],
          eventStarts: [],
          respGroups: [],
          responsibilities: []
        }
      };
    }
  }

  // Merge task data under the corresponding ticket
  for (var j = 1; j < taskData.length; j++) {
    var taskTicketID = taskData[j][3]; // Assuming Task's Ticket ID is in column D (index 3)

    if (ticketMap[taskTicketID]) {
      ticketMap[taskTicketID].tasks.ids.push(taskData[j][0] || ""); // Task ID
      ticketMap[taskTicketID].tasks.titles.push(taskData[j][1] || ""); // Task Title
      ticketMap[taskTicketID].tasks.createdDates.push(taskData[j][4] || ""); // Task Created
      ticketMap[taskTicketID].tasks.dueDates.push(taskData[j][5] || ""); // Task Due
      ticketMap[taskTicketID].tasks.eventStarts.push(taskData[j][6] || ""); // Event Start
      ticketMap[taskTicketID].tasks.respGroups.push(taskData[j][7] || ""); // Task Resp Group
      ticketMap[taskTicketID].tasks.responsibilities.push(taskData[j][8] || ""); // Task Responsibility
    }
  }

  // Convert map data into a single row per ticket, but only if it has tasks
  for (var ticketID in ticketMap) {
    var ticketEntry = ticketMap[ticketID];

    // **Filter out tickets that don't have tasks**
    if (ticketEntry.tasks.ids.length > 0) {
      mergedData.push([
        ...ticketEntry.ticketDetails,
        ticketEntry.tasks.ids.join(", "), // Task IDs combined
        ticketEntry.tasks.titles.join(", "), // Task Titles combined
        ticketEntry.tasks.createdDates.join(", "), // Task Created Dates combined
        ticketEntry.tasks.dueDates.join(", "), // Task Due Dates combined
        ticketEntry.tasks.eventStarts.join(", "), // Event Start Times combined
        ticketEntry.tasks.respGroups.join(", "), // Task Resp Groups combined
        ticketEntry.tasks.responsibilities.join(", ") // Task Responsibilities combined
      ]);
    }
  }

  // Write merged data to the new sheet
  mergedSheet.getRange(1, 1, mergedData.length, mergedData[0].length).setValues(mergedData);
}
