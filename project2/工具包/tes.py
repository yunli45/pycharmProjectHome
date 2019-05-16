from lxml import etree

wb_data = """
       <table width="95%" cellspacing="0" cellpadding="0" border="0" align="center">
                                                    
                                                      <tbody><tr>
                                                        <td style="font-size:14px; line-height:170%; padding-top:20px;" align="left"> 
                                                        <font id="Zoom">
                                                        			
				<p>海南省琼海市-_行政处罚(2018.12月份)</p><br>
			
							<script>
							var fujian1 = "海南省琼海市-_行政处罚(2018.12月份).xls"
							if(fujian1.length != "")
							{
								document.write("<b>附件列表</b>：");
							}
							</script><b>附件列表</b>：
							<b><a href="./P020190114624769074502.xls">海南省琼海市-_行政处罚(2018.12月份).xls</a></b>
			
                                                        </font></td>
                                                      </tr>
                                                    
                                                </tbody></table>
        """
html = etree.HTML(wb_data)
html_data = str(html.xpath('/html/body/table/text()'))
# html_data =  etree.tostring(html_data)

print(html_data)
