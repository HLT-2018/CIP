#include<stdio.h>
#include<process.h>
 /*�˳�������ʶ��GB����ĺ��ֺ������������ַ�������ռ�����ֽڣ�
 �����������ַ�ռһ���ֽ�,�ж��Ǻ��ֻ��ǵ������ַ���
 ֻ��Ҫ��������ɨ���һ���ֽڵĵ�һλ�������0�����ʾ�Ƕ������ַ��������1�����Ǻ���*/ 
main(){
	FILE *fp;
	char ch[2];
	char a;
	fp=fopen("GB.txt","r");//�ļ�����ΪGB.txt 
	a=fgetc(fp);
	int count=0;
	while(a!=EOF){//��ASCII�ַ� 
		char b = a;
		int t=(b>>7)&1;
		if(t==0){
		count++;
		printf("%c ",a);
		a=fgetc(fp);
		}
		if(t==1){//�Ǻ��� 
			ch[0]=a;
			a=fgetc(fp);
			ch[1]=a;
			count++;
			printf("%s ",ch);
			a=getc(fp);
		}
		if((a>=-1&&a<48)||a>122){
			a=fgetc(fp); 
			count++;
		}
	}
	fclose(fp);
	printf("\n����character��%d��",count);
} 
