#include <stdio.h>
/*�˳�������ʶ��UTF-8����ĺ��ֺ������������ַ���UTF-8��1-6�ֽڱ�ʾһ���ַ���������Ҫ�������ҽ���ɨ��
���ݵ�ǰ�ֽڵ�ǰ��λ��������ǰ�ַ��ɶ��ٸ��ֽ���ɣ��ֱ��������������Ӧ���ֽ�����6��1�ݼ����Ӷ����Էֳ����е�����*/ 
main()
{
    FILE *fp = fopen("utf-8.txt","r");//���Լ�����Ϊ123.txt 
    char ch = getc(fp);
    int count=0;
    while (ch!= EOF)
    {
        int test = ch & 0xff;
        if(test>=0xfc)//һ�����������ֽ���ɵ���� 
		{
			printf("%c",ch);
            for(int i=0 ; i<5 ; i++)
            {
                ch = getc(fp);
                printf("%c",ch);
            }
            printf("  ");
            count++;
            ch = getc(fp);
            continue;
        	
		}
		else if(test >= 0xf8 && test<0xfc)//һ����������ֽ���ɵ����
		{
			printf("%c",ch);
            for(int i=0 ; i<4 ; i++)
            {
                ch = getc(fp);
                printf("%c",ch);
            }
            printf("  ");
            count++;
            ch = getc(fp);
            continue;
		}
        else if(test>=0xf0 && test<0xf8)//һ�������ĸ��ֽ���ɵ����
        {
            printf("%c",ch);
            for(int i=0 ; i<3 ; i++)
            {
                ch = getc(fp);
                printf("%c",ch);
            }
            printf("  ");
            count++;
            ch = getc(fp);
            continue;
        }
        else if(test >= 0xe0 && test < 0xf0)//һ�����������ֽ���ɵ����
		{
            printf("%c",ch);
            for(int i=0 ; i<2 ; i++)
            {
                ch = getc(fp);
                printf("%c",ch);
            }
            printf("  ");
            count++;
            ch = getc(fp);
            continue;
        }
        else if(test >= 0xc0 && test <0xe0)//һ�����������ֽ���ɵ����
		{
            printf("%c",ch);
            ch = fgetc(fp);
            printf("%c  ",ch);
            count++;
            ch = fgetc(fp);
            continue;
        }
        else//һ������һ���ֽ���ɵ����
        {
            printf("%c  ",ch);
            count++;
            ch = getc(fp);
            continue;
        }
    }
    printf("\n");
    printf("%d",count);
    fclose(fp);
}
