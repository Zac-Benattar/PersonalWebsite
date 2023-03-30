class DateStringifier {
  constructor(date) {
    this.date = date;
  }

  static getTimeFromUNIXTimestampSeconds(unixTimestamp) {
    // Turning unix timestamp into a nicely formatted string
    const date = new Date(unixTimestamp * 1000);
    var dateString = "";

    // If number of hours in the date is zero, append another zero to the end to get e.g. 00:30 rather than 0:30
    if (date.getUTCHours() === 0) {
      dateString += date.getUTCHours() + "0";
    } else if (date.getUTCHours() > 0 && date.getUTCHours() < 10) {
      dateString += "0" + date.getUTCHours();
    } else {
      dateString += date.getUTCHours();
    }

    dateString += ":";

    // If number of minutes in the date is zero, append another zero to the end to get e.g. 12:00 rather than 12:0
    if (date.getUTCMinutes() === 0) {
      dateString += date.getUTCMinutes() + "0 ";
    } else if (date.getUTCMinutes() > 0 && date.getUTCMinutes() < 10) {
      dateString += "0" + date.getUTCMinutes();
    } else {
      dateString += date.getUTCMinutes();
    }

    return dateString;
  }

  static getFullDateFromUNIXTimestampSeconds(unixTimestamp) {
    const date = new Date(unixTimestamp * 1000);
    var dateString = this.getTimeFromUNIXTimestampSeconds(unixTimestamp);
    return (dateString +=
      " " +
      date.getUTCDate() +
      "/" +
      date.getUTCMonth() +
      "/" +
      date.getUTCFullYear());
  }
}

export default DateStringifier;
