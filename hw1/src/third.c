#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/moduleparam.h>

MODULE_LICENSE("GPL");

static char *myname = "Professor_Liao";
module_param(myname, charp, 0000);
MODULE_PARM_DESC(myname, "Dongrui");

static int myage = 0;
module_param(myage, int, 0000);
MODULE_PARM_DESC(myage, "23");

static char *birthday = "1,1";
module_param(birthday, charp, 0000);
MODULE_PARM_DESC(birthday, "11,22");

static int __init proc_init(void){
	int month = 1, day = 1;
	sscanf(birthday, "%d,%d", &month, &day);

	pr_info("Hello world\n");
	pr_info("My name is: %s\n", myname);
	pr_info("My age is %d\n", myage);
	pr_info("My birthday is: %d/%d\n", month, day);

	return 0;
}

static void __exit proc_exit(void){
	pr_info("Goodbye, world\n");
}

module_init(proc_init);
module_exit(proc_exit);
