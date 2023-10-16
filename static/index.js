document.addEventListener('DOMContentLoaded', function () {
            var srcElements = document.getElementsByClassName("m2");
            const array = Array.from(srcElements);
            
            array.forEach(function (element) {
                var text = element.textContent;
                var words = text.split(' ');
                words.forEach(function (word, index) {
                    var info;
                    if (word.includes('+++')) {
                        info = word.split("+++")
                        words[index] = '<span title="'+info[0]+'" style="background-color: yellowgreen;">' + info[1] + '</span>';
                    }
                    if (word.includes('---')) {
                        info = word.split("---")
                        words[index] = '<span title="'+info[0]+'" style="background-color: pink;">' + info[1] + '</span>';
                    }
                    if (word.includes("???")) {
                        info = word.split("???")
                        words[index] = '<span title="'+info[0]+'" style="background-color: yellow;">' + info[1] + '</span>';
                    }
                });
                
                var coloredText = words.join(' ');
                element.innerHTML = coloredText;
            });
        });