from case.IssueCheck.common_issuecheck import Test_LiaisonMan
import pytest

@pytest.mark.parametrize('test_data1',['1','2']) #业务类型：1审核业务，2处置业务.
@pytest.mark.parametrize('test_data2',['1','1,2','1,2,3']) #消息媒介：1站内 2钉消息 3短信
def test_addliaisonman(login_fix,delete_all_liaisonman,test_data1,test_data2):
    '''新增联络员：业务类型和消息媒介组合新增所有的测试用例'''
    re = Test_LiaisonMan(login_fix)
    res = re.addliaisonman(test_data1,test_data2)
    assert res['code']==200
    assert res['message'] == '保存成功'

@pytest.mark.parametrize('test_data1',['','1','2'])#业务类型：1审核业务，2处置业务,''空为全部
@pytest.mark.parametrize('test_data2',['杨一帆1',''])
@pytest.mark.parametrize('test_data3',['330782000000_11330782097919258G',''])
@pytest.mark.parametrize('test_data4',['13588012414',''])
def test_selectliaisonman(login_fix,delete_all_liaisonman,test_data1,test_data2,test_data3,test_data4):
    '''查询联络员：业务分类、机构名称、联络员姓名、联系方式组合查询'''
    r = Test_LiaisonMan(login_fix)
    add = r.addliaisonman(businessType=1, remindType=1)
    res = r.selectliaisonman(test_data1,test_data2,test_data3,test_data4)
    assert res['code'] == 200
    assert res['message'] == '查询成功'

def test_editliaisonman(login_fix,delete_all_liaisonman):
    '''修改联络员：修改消息媒介'''
    r = Test_LiaisonMan(login_fix)
    add = r.addliaisonman(businessType=1, remindType=1)
    res = r.editliaisonman(remindType='1,2')
    assert res['code'] == 200
    assert res['message'] == '编辑成功'

def test_deleteliaisonman(login_fix):
    '''删除联络员：以新增clueliaid删除联络员'''
    r = Test_LiaisonMan(login_fix)
    add = r.addliaisonman(businessType=1, remindType=1)
    res = r.selectliaisonman()
    id = res['data']['data'][0]['clueliaid']
    res = r.deleteliaisonman(clueliaid=id)
    assert res['code'] == 200
    assert res['message'] == '删除成功'

if __name__ == '__main__':
    pytest.main(['-v','--setup-show','-k','delete','test_LiaisonMan.py'])