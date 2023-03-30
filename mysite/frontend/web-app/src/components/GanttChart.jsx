import React from "react";
import Chart from "react-google-charts";
import "../pages/tasks.css";
//append array of tasks to ganttChartData const

//ganttChartData const stores array of task arrays

//first element is array of gantt chart data fields (do not change)

//task id unique identifier for each task
//task name is name of task (does not have to be unique but recommend is quite short for for better formatting)

//duration is converted from milliseconds to days
//---> number of days * 24 * 60 * 60 * 1000 = number of milliseconds
//---> this number will then be converted and displayed as number of days
//duration defaults to time between start and end date if left null

//completion status is measured as a percentage of completion
//we do not store data on the task percentage completion - assign arbitrary values to completion status categories instead
//e.g. 50 = started but not completed

//dependecies takes a string containing a list of task ids of tasks that are dependent
//only include tasks dependent on the current task not tasks the current task is dependent on
//dependencies in the depencies string are separated by a comma only (no spaces)
//format of depencies string --> 'dependency1taskid,dpendency2taskid'

const GanttChart = ({ tasks }) => {
  // Some of this are compatable, many are not with the required format
  const ganttChartData = tasks.map((task) => {
    let dependentTasksString = task.dependent_tasks_string;
    if (task.dependent_tasks_string === "") {
      dependentTasksString = null;
    }

    return [
      task.id.toString(),
      task.name,
      new Date(task.start_date_unix * 1000),
      new Date(task.latest_finish_date_unix * 1000),
      null,
      task.completion,
      dependentTasksString,
    ];
  });

  const columns = [
    { type: "string", label: "Task ID" },
    { type: "string", label: "Task Name" },
    { type: "date", label: "Start Date" },
    { type: "date", label: "End Date" },
    { type: "number", label: "Duration" },
    { type: "number", label: "Percent Complete" },
    { type: "string", label: "Dependencies" },
  ];

  var data = [columns, ...ganttChartData];

  const ganttChartExampleData = [
    [
      { type: "string", label: "Task ID" },
      { type: "string", label: "Task Name" },
      { type: "date", label: "Start Date" },
      { type: "date", label: "End Date" },
      { type: "number", label: "Duration" },
      { type: "number", label: "Percent Complete" },
      { type: "string", label: "Dependencies" },
    ],
    [
      "Research",
      "Find sources",
      new Date(2015, 0, 1),
      new Date(2015, 0, 5),
      null,
      100,
      null,
    ],
    [
      "Write",
      "Write paper",
      null,
      new Date(2015, 0, 9),
      3 * 24 * 60 * 60 * 1000,
      25,
      "Research,Outline",
    ],
    [
      "Cite",
      "Create bibliography",
      null,
      new Date(2015, 0, 7),
      1 * 24 * 60 * 60 * 1000,
      20,
      "Research",
    ],
    [
      "Complete",
      "Hand in paper",
      null,
      new Date(2015, 0, 10),
      1 * 24 * 60 * 60 * 1000,
      0,
      "Cite,Write",
    ],
    [
      "Outline",
      "Outline paper",
      null,
      new Date(2015, 0, 6),
      1 * 24 * 60 * 60 * 1000,
      100,
      "Research",
    ],
  ];

  console.log(ganttChartExampleData)
  console.log(data)

  return (
    <div className="gantt-view-container">
    <div className="gantt-chart">
      <Chart
        width={"700px"}
        height={"410px"}
        chartType="Gantt"
        loader={<div>Loading Chart</div>}
        data={data}
        rootProps={{ "data-testid": "1" }}
      />
    </div>
    </div>
  );
};

export default GanttChart;
