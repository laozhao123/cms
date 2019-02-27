var vm = new Vue({
    el: '#app',
    data: {
        // 双向绑定变量
        username: '',
        password: '',
        password2: '',
        mobile: '',
        sms_code: '',
        allow: false,

        // 控制元素是否显示
        error_name: false,
        error_password: false,
        error_check_password: false,
        error_phone: false,
        error_sms_code: false,
        error_allow: false,
        sending_flag:false,

        // 出错提示
        error_name_message: '请输入5-20个字符的用户名',
        error_password_message: '请输入8-20位的登录密码',
        error_phone_message: '请输入正确的手机号',
        error_sms_code_message: '请输入短信验证码',

        // 图片验证码
        image_code_id: '',
        image_code_url: '',
    },

    // 当vue实例挂载到界面后执行, 可以在此方法中执行界面初始化操作
    mounted: function () {

    },

    methods: {
        check_username: function () {
            var len = this.username.length;
            if (len < 5 || len > 20) {
                this.error_name = true;
            } else {
                this.error_name = false;
            }

            if (this.error_name == false){

                axios.get('http://127.0.0.1:8000/usernames/'+this.username+'/count/')
                    .then(response=>{
                        if(response.data['count'] !=0){
                            this.error_name = true;
                            this.error_name_message='用户名已存在';
                        }else {
                             this.error_name = false;
                        }
                    })
                    .catch(error=>{
                        console.log(error.response)
                    })


            }
        },

        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },

        check_cpwd: function () {
            if (this.password !== this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },

        check_phone: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.mobile)) {

                this.error_phone = false;
            } else {
                this.error_phone = true;
            }
        },

        check_sms_code: function () {
            var len = this.sms_code.length;
            if (len === 0) {
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },

        check_allow: function () {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },

        // 获取短信
        get_sms_code: function() {
            this.check_phone();

            if (this.sending_flag){
                return
            }

            if (!this.error_phone) {
				//发送获取请求
                this.sending_flag=true;
				axios.get('http://127.0.0.1:8000/sms_codes/'+this.mobile+'/')
                    .then(response=>{
                        var num=60;
                        var t=setInterval(()=>{
                            if (num==1){
                                clearInterval(t);
                                 // 将点击获取验证码的按钮展示的文本恢复成原始文本
                                this.error_sms_code_message = '获取短信验证码';
                                // 将点击按钮的onclick事件函数恢复回去
                                this.sending_flag = false;
                            }else {
                            num -= 1;
                            // 展示倒计时信息
                            this.error_sms_code_message = num + '秒';
                             }
                         }, 1000, 60);
                    })
                    .catch(error=>{
                        // 显示出错信息
                        this.error_sms_code = true;
                        this.error_sms_code_message = error.response.data.message;
                        this.sending_flag = false;
                    })
            }
        },

        // 点击注册按钮
        on_submit: function () {

            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_phone();
            this.check_allow();

            if (this.error_name === false
                && this.error_password === false
                && this.error_check_password === false
                && this.error_phone === false
                && this.error_allow === false) {
				//发送注册请求
                var data = {
                        username: this.username,
                        password: this.password,
                        password2: this.password2,
                        mobile: this.mobile,
                        sms_code: this.sms_code,
                        allow: this.allow
                    };
                axios.post('http://127.0.0.1:8000/register/',data)
                    .then(response=>{
                        location.href = '/index.html';      // 跳转到首页
                    })
                    .catch(error=>{
                        if (error.response.status === 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_sms_code = true;
                                this.error_sms_code_message = error.response
                                    .data.non_field_errors[0];
                            } else {
                                alert('注册失败')
                            }
                        }
                    })


            } else {
                 alert('填写有误')
            }
        },
    }
});

