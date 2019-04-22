### Create a `Cron` job for automatic mysql dump generation
 - Create a <filename>.sh file
   - mysqldump --no-defaults -u root -p<password> <db_name> <table_names> | gzip > /path/to/back_up_folder/<dump_file_name>_`date +%F`.sql.gz
 - Provide execute permission
   - chmod +x /path/to/<file_name>.sh
 - Run command `sudo crontab -e`
 - Add `30 23 * * * /path/to/<file_name>.sh` to `.sh` file
