var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        token: sessionStorage.token || localStorage.token,

        addresses: [],      // 当前登录用户的地址列表
        user_id: 0,         // 当前登录用户的id
        default_address_id: '',     // 当前登录用户的默认地址的id
    },

    mounted: function(){
        // 请求当前登录用户的所有的地址
       config={
                     headers: {
                    'Authorization': 'JWT ' + this.token
                }
                };
                    axios.get('http://127.0.0.1:8000/address/',config)
                        .then(response=>{
                            this.addresses=response.data['addresses'];
                            this.default_address_id=response.data['default_address_id'];
                        })
                        .catch(error=>{
                            console.log(error.response.data);
                        })
    },

    methods: {
        // 设置默认地址
        set_default: function(){
            if (!this.default_address_id) {
                alert('请先选择默认地址');
                return
            }
			//发送请求
            config={
                     headers: {
                    'Authorization': 'JWT ' + this.token
                }
                };
                  axios.put('http://127.0.0.1:8000/setaddr/'+this.default_address_id+'/',{},config)
                        .then(response=>{
                            alert('以保存');
                        })
                        .catch(error=>{
                            console.log(error.response.data);
                        })
           
        },

        // 删除地址
        delete_address: function (address_id) {
            // 发送请求
             config={
                     headers: {
                    'Authorization': 'JWT ' + this.token
                }
                };
                  axios.delete('http://127.0.0.1:8000/address/'+address_id+'/',config)
                        .then(response=>{
                            alert('已删除');
                        })
                        .catch(error=>{
                            console.log(error.response.data);
                        })

            
        }
    }
});